import zipfile
import os
import tempfile
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import streamlit as st
import yaml
import google.generativeai as genai
from google.api_core import retry


def load_config():
    config_file = "config.yaml"
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    else:
        st.error("Configuration file not found. Please ensure 'config.yaml' is present.")
        return None

def extract_txt_from_zip(zip_file, start_date, end_date):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            txt_file_path = extract_files_from_zip(zip_file, tmpdirname)
            if txt_file_path:
                return read_and_filter_txt(txt_file_path, start_date, end_date)
            else:
                st.error('No .txt file found in the uploaded .zip.')
                return None
    except zipfile.BadZipFile:
        st.error('The uploaded file is not a valid zip file.')
        return None

def extract_files_from_zip(zip_file, extract_to):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            txt_files = [
                os.path.join(root, file)
                for root, _, files in os.walk(extract_to)
                for file in files if file.endswith('.txt')
            ]
            return txt_files[0] if txt_files else None
    except Exception as e:
        st.error(f"Error extracting files: {e}")
        return None

def read_and_filter_txt(txt_file_path, start_date, end_date):
    for encoding in ['utf-8', 'utf-8-sig', 'utf-16', 'latin-1']:
        try:
            start_date = datetime.strptime(start_date, "%d/%m/%y")
            end_date = datetime.strptime(end_date, "%d/%m/%y")

            trimmed_text = ""
            include_message = False
            with open(txt_file_path, "r", encoding=encoding) as file:
                for line in file:
                    match = re.match(r"(\d{2}/\d{2}/\d{2}),", line)
                    if match:
                        date_str = match.group(1)
                        message_date = datetime.strptime(date_str, "%d/%m/%y")
                        include_message = start_date <= message_date <= end_date

                    if include_message:
                        trimmed_text += line

            return trimmed_text
        except UnicodeDecodeError:
            continue
    st.error('Unable to read the .txt file with common encodings.')
    return None

def analyze_chat_file(file_content, start_date, end_date):
    message_times = []

    for line in file_content.splitlines():
        message_time = parse_line(line)
        if message_time:
            message_times.append(message_time)

    hourly_fig = plot_message_distribution(message_times, start_date, end_date)
    weekday_fig = plot_weekday_distribution(message_times, start_date, end_date)
    return hourly_fig, weekday_fig

def plot_message_distribution(message_times, start_date, end_date):
    hours = [msg_time.hour for msg_time in message_times]
    hour_counts = Counter(hours)
    hours_range = range(24)
    counts = [hour_counts.get(hour, 0) for hour in hours_range]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hours_range, counts, color='skyblue')
    ax.set_xlabel('Hora do Dia')
    ax.set_ylabel('Número de Mensagens')
    ax.set_title(f'Distribuição das Mensagens no período ({start_date} a {end_date})')
    ax.set_xticks(hours_range)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig

def plot_weekday_distribution(message_times, start_date, end_date):
    weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    days = [msg_time.weekday() for msg_time in message_times]
    day_counts = Counter(days)
    counts = [day_counts.get(day, 0) for day in range(7)]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(weekdays, counts, color='lightgreen')
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Número de Mensagens')
    ax.set_title(f'Distribuição das Mensagens por Dia da Semana ({start_date} a {end_date})')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig

def parse_line(line):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(AM|PM|am|pm|a\.m\.|p\.m\.)?\s?-'
    match = re.match(pattern, line)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        am_pm = match.group(3)
        datetime_str = f"{date_str} {time_str}"
        if am_pm:
            datetime_str += f" {am_pm}"
            time_format = '%d/%m/%y %I:%M %p'
        else:
            time_format = '%d/%m/%y %H:%M'
        try:
            return datetime.strptime(datetime_str, time_format)
        except ValueError:
            pass
    return None

retry_policy = {
    "retry": retry.Retry(predicate=retry.if_transient_error, initial=10, multiplier=1.5, timeout=300)
}

def generate_ai_response(model_version, prompt, text):
    print(model_version)
    try:
        model = genai.GenerativeModel(
                model_version,
                generation_config=genai.types.GenerationConfig(temperature=0.7))
        ai_prompt = prompt + '\n\n"""\n' + text + '\n"""'
        st.write(model.count_tokens(ai_prompt))
        response = model.generate_content(
            ai_prompt,
            request_options=retry_policy
        )
        return response
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return None

def main():
    st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
    
    st.title("WhatsApp Chat Analyzer")
    st.write("Upload a zip file containing WhatsApp chat exports and specify the date range for analysis.")

    config = load_config()
    if config is None:
        return

    google_api_key = config.get('GOOGLE_API_KEY')
    if google_api_key:
        genai.configure(api_key=google_api_key)
    else:
        st.error("GOOGLE_API_KEY is not configured in the config file.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload Zip File", type=["zip"])
        
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date = st.date_input("Start Date", disabled=not uploaded_file)
        with date_col2:
            end_date = st.date_input("End Date", disabled=not uploaded_file)
        
        if start_date and end_date:
            start_date = start_date.strftime('%d/%m/%y')
            end_date = end_date.strftime('%d/%m/%y')

    with col2:
        st.subheader("AI Configuration")
        models = genai.list_models()
        model_names = [model.name for model in models]
        default_model_index = model_names.index(config.get('MODEL_VERSION', model_names[0])) if config.get('MODEL_VERSION', model_names[0]) in model_names else 0
        
        model_version = st.selectbox("AI Model Version", model_names, index=default_model_index)

    st.subheader("AI Prompt")
    default_prompt = config.get('DEFAULT_PROMPT', '')
    prompt = st.text_area("Enter your prompt here:", value=default_prompt, height=150,
                          help="Customize the prompt for the AI analysis. Use placeholders like {start_date} and {end_date} if needed.")
    
    # Replace placeholders in the prompt
    prompt = prompt.replace("{start_date}", start_date).replace("{end_date}", end_date)

    col1, col2 = st.columns(2)
    with col1:
        plot_button = st.button("📊 Generate Plot", use_container_width=True, disabled=not uploaded_file)
    with col2:
        ai_button = st.button("🤖 Generate AI Response", use_container_width=True, disabled=not uploaded_file)


    if plot_button:
        if uploaded_file and start_date and end_date:
            content = extract_txt_from_zip(uploaded_file, start_date, end_date)
            if content:
                st.success("Chat data extracted successfully!")
                hourly_fig, weekday_fig = analyze_chat_file(content, start_date, end_date)
                st.pyplot(hourly_fig)
                st.pyplot(weekday_fig)
            else:
                st.error("No content found for the specified date range.")
        else:
            st.warning("Please provide all required inputs.")

    if ai_button:
        if uploaded_file and start_date and end_date and model_version and prompt:
            content = extract_txt_from_zip(uploaded_file, start_date, end_date)
            if content:
                with st.spinner("Generating AI response, this might take a while..."):
                    response = generate_ai_response(model_version, prompt, content)
                    if response:
                        st.divider()
                        st.subheader("AI Response (using " + model_version + ")")
                        st.markdown(response.text)

                        expander = st.expander("Ver markdown")
                        expander.code(response.text)                    
            else:
                st.error("No content found for the specified date range.")
        else:
            st.warning("Please provide all required inputs, including AI model version and prompt.")

if __name__ == "__main__":
    main()