import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime
import yaml
from jinja2 import Environment, FileSystemLoader


def render_latex(profile, jobdesc, template_path="templates/resume.tex.j2", output_name="resume.tex", graphics=True,
                 swap_columns=False):
    template_path = Path(template_path)
    template_dir = template_path.parent
    template_file = template_path.name

    # The output will be written to the current working directory or a specified path
    # based on the output_name argument
    env = Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
    )
    template = env.get_template(template_file)

    context = {
        "today": datetime.now(),
        "graphics": graphics,
        "personal": profile["personal"],
        "education": profile.get("education", []),
        "skill_groups": profile.get("skill_groups", []),
        "experience": profile.get("experience", []),
        "interests": profile.get("interests", []),
        "languages": profile.get("languages", []),
        "practices": profile.get("practices", []),
        "achievements": profile.get("achievements", []),
        "certifications_and_training": profile.get("certifications_and_training", []),
        "swap_columns": swap_columns,
        "cover_letter": profile.get("cover_letter", {}),
    }

    tex = template.render(context)

    # Write to the filename provided in the arguments
    out_path = Path(output_name)
    out_path.write_text(tex)

    print(f"File generated: {out_path}")


def load_profile(path="profile.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def parse_job_description(text):
    # extract keywords (naive split)
    words = re.findall(r"\b[A-Za-z]+\b", text.lower())
    return set(words)


def tailor(profile, job_desc):
    jd_keywords = parse_job_description(job_desc)

    # Search through nested categories and descriptions
    relevant_groups = []
    for group in profile.get("skill_groups", []):
        matched_entries = [
            e for e in group["entries"]
            if any(w in e["label"].lower() or w in e["desc"].lower() for w in jd_keywords)
        ]
        if matched_entries:
            # Keep the group but only with relevant skills
            relevant_groups.append({**group, "entries": matched_entries})

    return {
        "skill_groups": relevant_groups or profile["skill_groups"][:3],
        "experience": profile["experience"][:2], # simplified for now
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jobdesc", help="Path to job description text")
    parser.add_argument("--profile", default="profiles/default.yaml")
    parser.add_argument("--templatefile", default="templates/resume.tex.j2")
    parser.add_argument("--graphics", action="store_true", help="Enable graphics/logos in output")
    parser.add_argument("--swap-columns", action="store_true", help="Swap the left and right columns")
    parser.add_argument("--output", default="resume.tex", help="Name of the output .tex file")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    jobdesc_text = Path(args.jobdesc).read_text()

    # We now pass args.output to the render function
    render_latex(
        profile,
        jobdesc_text,
        template_path=args.templatefile,
        output_name=args.output,
        graphics=args.graphics,
        swap_columns=args.swap_columns
    )

if __name__ == "__main__":
    main()
