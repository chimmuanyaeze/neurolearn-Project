# 📚 NeuroLearn STEM Visualizer

NeuroLearn STEM Visualizer is an interactive Streamlit application that provides AI-powered tutoring and generates video-based explanations for STEM (Science, Technology, Engineering, and Mathematics) problems. Users can chat with an AI tutor, submit problems, and receive detailed, visual solutions to enhance their understanding.

## ✨ Features

* **AI-Powered Tutoring:** Engage in a conversational chat with an AI assistant for STEM queries.
* **Video Explanations:** Receive automatically generated video solutions for complex problems.
* **Supabase Integration:** Secure user authentication and persistent chat history storage using Supabase.
* **Free Usage Tier:** Limited free uses for unauthenticated users, with full access upon login.
* **Intuitive UI:** Built with Streamlit for a simple and responsive user experience.

## 🚀 Getting Started

Follow these steps to set up and run the NeuroLearn STEM Visualizer locally.

### Prerequisites

* Python 3.8+
* Git (for cloning the repository)

### Installation

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME # e.g., cd neurolearn-stem-visualizer
    ```

    *(Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.)*

2. **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source ./.venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Make sure you have a `requirements.txt` file in your root directory listing all Python packages used, e.g., `streamlit`, `st-supabase-connection`, `streamlit-supabase-auth`, `langchain`, `openai`, `moviepy`, etc.)*

### Supabase Setup

This application relies on Supabase for authentication and database storage.

1. **Create a Supabase Project:**
    * Go to [Supabase](https://supabase.com/) and create a new project.
    * Note down your project URL and your `anon` public key (found under Project Settings -> API).

2. **Configure `secrets.toml`:**
    * In your project's root directory, create a folder named `.streamlit`.
    * Inside `.streamlit`, create a file named `secrets.toml`.
    * Add your Supabase credentials to this file in the following format:

        ```toml
        [connections.supabase]
        SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
        SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

        [auth.supabase]
        url = "YOUR_SUPABASE_PROJECT_URL"
        key = "YOUR_SUPABASE_ANON_KEY"
        ```

        *(Replace `YOUR_SUPABASE_PROJECT_URL` and `YOUR_SUPABASE_ANON_KEY` with your actual Supabase project details.)*

3. **Database Schema (Optional - for chat history persistence):**
    * If you plan to persist chat history, you'll need a `chats` table in your Supabase database. Here's a basic SQL schema:

        ```sql
        CREATE TABLE public.chats (
          id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
          user_id UUID REFERENCES auth.users (id) ON DELETE CASCADE,
          title TEXT,
          history JSONB, -- Stores the chat conversation as a JSON array of messages
          created_at TIMESTAMPTZ DEFAULT NOW()
        );

        -- Optional: RLS (Row Level Security) policies for 'chats' table
        ALTER TABLE public.chats ENABLE ROW LEVEL SECURITY;

        CREATE POLICY "Enable read access for all users"
        ON public.chats FOR SELECT
        TO authenticated
        USING (true);

        CREATE POLICY "Enable insert for authenticated users only"
        ON public.chats FOR INSERT
        TO authenticated
        WITH CHECK (auth.uid() = user_id);

        CREATE POLICY "Enable update for users based on user_id"
        ON public.chats FOR UPDATE
        TO authenticated
        USING (auth.uid() = user_id);

        CREATE POLICY "Enable delete for users based on user_id"
        ON public.chats FOR DELETE
        TO authenticated
        USING (auth.uid() = user_id);
        ```

    * Ensure your `auth.users` table is correctly set up by Supabase's authentication services.

### Running the App

Once setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
