import streamlit as st
from phi.tools.youtube_tools import YouTubeTools
from agent import get_chunk_summarizer, get_video_summarizer


def main():
    # Set up interface
    st.set_page_config(page_title="Summarize Tool", page_icon=":heart:")
    st.title("Youtube Video Summarizer")    
    st.markdown("##### :handshake: This tool is built using [phidata](https://docs.phidata.com/agents) framework and powered by [Groq](https://groq.com)")
    st.write("Paste the youtube video url into the textbox, click the button and wait for the summarization")
    
    # Get model
    llm_model = st.selectbox(
        ":brain: Select Model", 
        options=["llama3-70b-8192", 
                 "llama3-8b-8192",
                 "llama3-groq-70b-8192-tool-use-preview	",
                 "llama-3.1-70b-versatile",
                 "llama-3.1-8b-instant",
                 "llama-3.2-3b-preview",
                 "llama-3.2-90b-vision-preview",
                 "gemma2-9b-it",
                 "mixtral-8x7b-32768"]
    )
    ## Set agent_type in session state
    if "llm_model" not in st.session_state:
            st.session_state["llm_model"] = llm_model
    elif st.session_state["llm_model"] != llm_model:
        st.session_state["llm_model"] = llm_model
        st.rerun()

    # Set characters limit in each chunk
    chunk_limit = st.slider(
        ":heart_on_fire: Words in chunk",
        min_value = 1000,
        max_value = 10000,
        value = 2000,
        step = 500,
        help = "Set the word limit for each chunk, allowing the model to summarize sections separately before combining.",
    )
    
    # Set length of the summary
    summary_type = st.radio(":gear: Select Type", ["Long", "Short"])

    # Get video url and generate report
    video_url = st.text_input(":video_camera: Video URL")
    generate_report = st.button("Generate Summary")

    ## Save url in session state
    if generate_report:
        st.session_state["youtube_url"] = video_url

    if "youtube_url" in st.session_state:
        _url = st.session_state["youtube_url"]
        youtube_tools = YouTubeTools(languages=["en"])
        video_summarizer = get_video_summarizer(model=llm_model, summary_type=summary_type)
        
        ### Show video information
        with st.status("Parsing Video", expanded=False) as status:                     
            video_data = youtube_tools.get_youtube_video_data(_url)
            with st.container():
                video_container = st.empty()
                video_container.video(_url)
                video_data_container = st.empty()
                video_data_container.json(video_data)
            status.update(label="Video information", state="complete", expanded=False)

        ### Show video captions
        with st.status("Reading Captions", expanded=False) as status:
            video_captions = youtube_tools.get_youtube_video_captions(_url)
            if not video_captions:
                st.write("Sorry could not parse video. Please try again or use a different video.")
                return
            
            with st.container():
                video_captions_container = st.empty()
                video_captions_container.write(video_captions)
            status.update(label="Captions", state="complete", expanded=False)

        ### Show summary
        chunks = []
        num_chunks = 0
        words = video_captions.split()
        for i in range(0, len(words), chunk_limit):
            num_chunks += 1
            chunks.append(" ".join(words[i : (i + chunk_limit)]))
        
        if num_chunks > 1:
            chunk_summaries = []
            for i in range(num_chunks):
                with st.status(f"Summarizing chunk {i+1}", expanded=False) as status:
                    chunk_summary = ""
                    chunk_container = st.empty()
                    chunk_summarizer = get_chunk_summarizer(model=llm_model)
                    chunk_info = f"Video data: {video_data}\n\n"
                    chunk_info += f"{chunks[i]}\n\n"
                    
                    for result in chunk_summarizer.run(chunk_info):
                        if result[0] == 'content':
                            chunk_summary += result[1]
                            chunk_container.markdown(chunk_summary)
                            
                    chunk_summaries.append(chunk_summary)
                    status.update(label=f"Chunk {i+1} summarized", state="complete", expanded=False)

            with st.spinner("Processing..."):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += "Chunk summaries:\n\n"
                
                for i, chunk_summary in enumerate(chunk_summaries, start=1):
                    video_info += f"Chunk {i}:\n\n{chunk_summary}\n\n"
                    video_info += "---\n\n"

                for result in video_summarizer.run(video_info):
                    if result[0] == 'content':
                        summary += result[1]
                        summary_container.markdown(summary)
        else:
            with st.spinner("Processing..."):
                summary = ""
                summary_container = st.empty()
                video_info = f"Video URL: {_url}\n\n"
                video_info += f"Video Data: {video_data}\n\n"
                video_info += f"Captions: {video_captions}\n\n"

                for result in video_summarizer.run(video_info):
                    if result[0] == 'content':
                        summary += result[1]
                        summary_container.markdown(summary)
    
        if st.button("Regenerate"):
            st.rerun()


if __name__ == "__main__":
    main()