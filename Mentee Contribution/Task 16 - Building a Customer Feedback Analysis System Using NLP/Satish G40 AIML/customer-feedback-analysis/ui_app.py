"""Simple GUI for customer feedback analysis using Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from main import analyze_feedback, ensure_models_exist


class FeedbackAnalysisApp:
    """Tkinter UI for the NLP feedback analysis project."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Customer Feedback Analysis")
        self.root.geometry("900x650")
        self.root.minsize(850, 600)

        self.root.configure(bg="#f3f6fb")

        title = tk.Label(
            root,
            text="CUSTOMER FEEDBACK ANALYSIS SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#f3f6fb",
            fg="#1f2d3d",
        )
        title.pack(pady=(20, 10))

        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(frame, text="Enter customer feedback:", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w")

        self.text_area = tk.Text(frame, height=10, width=110, font=("Arial", 11), wrap="word")
        self.text_area.pack(fill="x", pady=(5, 15))

        analyze_btn = tk.Button(
            frame,
            text="Analyze Feedback",
            command=self.run_analysis,
            bg="#2f80ed",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
        )
        analyze_btn.pack(anchor="w")

        result_frame = tk.LabelFrame(
            frame,
            text="Analysis Result",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=10,
            pady=10,
        )
        result_frame.pack(fill="both", expand=True, pady=(20, 5))

        self.result_text = tk.Text(result_frame, height=14, width=110, font=("Arial", 10), wrap="word")
        self.result_text.pack(fill="both", expand=True)
        self.result_text.configure(state="disabled")

    def run_analysis(self) -> None:
        """Analyze the text entered by the user and show the result in the UI."""
        feedback = self.text_area.get("1.0", "end").strip()

        if not feedback:
            messagebox.showwarning("Input required", "Please enter customer feedback before analyzing.")
            return

        try:
            result = analyze_feedback(feedback)
            sentiment = result["sentiment"]
            categories = result["categories"]
            keywords = result["keywords"]

            output = []
            output.append("====================================")
            output.append("CUSTOMER FEEDBACK ANALYSIS")
            output.append("====================================")
            output.append("")
            output.append(f"Feedback:\n{feedback}")
            output.append("")
            output.append(f"Sentiment:\n{sentiment}")
            output.append("")
            output.append("Categories:")
            if categories:
                for category in categories:
                    output.append(f"- {category}")
            else:
                output.append("- None detected")
            output.append("")
            output.append("Important Keywords:")
            if keywords:
                for keyword in keywords:
                    output.append(f"- {keyword}")
            else:
                output.append("- No keywords extracted")
            output.append("")
            output.append("====================================")

            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", "\n".join(output))
            self.result_text.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Error", f"An error occurred while analyzing the feedback: {exc}")


def main() -> None:
    """Start the Tkinter UI application."""
    ensure_models_exist()
    root = tk.Tk()
    app = FeedbackAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
