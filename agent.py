from textwrap import dedent
from phi.model.groq import Groq
from phi.agent import Agent


def get_chunk_summarizer(
    model
) -> Agent:
    """Get a Groq Research Agent."""

    return Agent(
        name = "groq_youtube_pre_processor",
        model = Groq(id=model),
        description = "You are a Senior NYT Reporter tasked with summarizing a youtube video.",
        instructions = [
            "You will be provided with a youtube video transcript.",
            "Carefully read the transcript a prepare thorough report of key facts and details.",
            "Provide as many details and facts as possible in the summary.",
            "Your report will be used to generate a final New York Times worthy report.",
            "Give the section relevant titles and provide details/facts/processes in each section."
            "REMEMBER: you are writing for the New York Times, so the quality of the report is important.",
            "Make sure your report is properly formatted and follows the <report_format> provided below.",
        ],
        add_to_system_prompt = dedent(
            """
        <report_format>
        ### Overview
        {give an overview of the video}

        ### Section 1
        {provide details/facts/processes in this section}

        ... more sections as necessary...

        ### Takeaways
        {provide key takeaways from the video}
        </report_format>
        """
        ),
        markdown = True,
        add_datetime_to_instructions = True,
        debug_mode = True,
    )


def get_video_summarizer(
    model,
    summary_type
) -> Agent:
    """Get a Groq Research Agent."""

    if summary_type == "Long":
        instructions = [
            "You will be provided with:"
            "  1. Youtube video link and information about the video"
            "  2. Pre-processed summaries from junior researchers."
            "Carefully process the information and think about the contents",
            "Then generate a final New York Times worthy report in the <report_format> provided below.",
            "Make your report engaging, informative, and well-structured.",
            "Break the report into sections and provide key takeaways at the end.",
            "Give the section relevant titles and provide details/facts/processes in each section."
            "Use markdown `#` syntax for headers, and place icons at the beginning of each header except the title.",
            "Example format for a header: `## 📖 Overview`",
            "Make sure the title has a `#` syntax and is presented as a markdown link to the video.",
            "REMEMBER: you are writing for the New York Times, so the quality of the report is important.",
        ]
        system_prompt = dedent(
            """
        <report_format>
        ## Video Title with Link
        {this is the markdown link to the video}

        ### Overview
        {give a brief introduction of the video and why the user should read this report}
        {make this section engaging and create a hook for the reader}

        ### Section 1
        {break the report into sections}
        {provide details/facts/processes in this section}

        ...more sections as necessary...

        ### Takeaways
        {provide key takeaways from the video}

        Report generated on: {Month Date, Year (hh:mm AM/PM)}
        </report_format>
        """
        )
    elif summary_type == "Short":
        instructions = [
            "You will be provided with:"
            "  1. Youtube video link and information about the video"
            "  2. Pre-processed summaries from junior researchers."
            "Carefully process the information and think about the contents",
            "Then generate a final New York Times worthy report in the <report_format> provided below.",
            "Make your report engaging, informative, and well-structured, ",
            "The report should includes only the overview and main takeaways.",
            "Use markdown `#` syntax for headers, and place icons at the beginning of each header except the title.",
            "Example format for a header: `## 📖 Overview`",
            "Make sure the title has a `#` syntax and is presented as a markdown link to the video.",
            "REMEMBER: you are writing for the New York Times, so the quality of the report is important.",
        ]
        system_prompt = dedent(
            """
        <report_format>
        ## Video Title with Link
        {this is the markdown link to the video}

        ### Overview
        {give a high-level overview of the video}

        ### Takeaways
        {provide key takeaways from the video}

        Report generated on: {Month Date, Year (hh:mm AM/PM)}
        </report_format>
        """
        )
        
    return Agent(
        name = "groq_video_summarizer",
        model = Groq(id=model),
        description = "You are a Senior NYT Reporter tasked with writing a summary of a youtube video.",
        instructions = instructions,
        add_to_system_prompt = system_prompt,
        markdown = True,
        add_datetime_to_instructions = True,
        debug_mode = True,
    )