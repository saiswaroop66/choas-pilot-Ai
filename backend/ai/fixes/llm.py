import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CHAOSPILOT LLM CLIENT
# =========================================================

class LLMClient:

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):

        # -------------------------------------------------
        # API KEY
        # -------------------------------------------------

        self.api_key = (
            api_key
            or os.getenv("GROQ_API_KEY")
        )


        # -------------------------------------------------
        # MODEL
        # -------------------------------------------------

        self.model = (
            model
            or os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-120b"
            )
        )


        # -------------------------------------------------
        # CLIENT
        # -------------------------------------------------

        self.client = None


        if self.api_key:

            self.client = Groq(
                api_key=self.api_key
            )


    # =====================================================
    # CHECK CONFIGURATION
    # =====================================================

    def is_configured(self) -> bool:

        return (
            self.client is not None
            and bool(self.api_key)
        )


    # =====================================================
    # GET MODEL
    # =====================================================

    def get_model(self) -> str:

        return self.model


    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 3000
    ) -> str:

        # -------------------------------------------------
        # CONFIGURATION CHECK
        # -------------------------------------------------

        if not self.is_configured():

            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Add GROQ_API_KEY to your .env file."
            )


        # -------------------------------------------------
        # VALIDATE PROMPTS
        # -------------------------------------------------

        if not system_prompt:

            raise ValueError(
                "System prompt cannot be empty."
            )


        if not user_prompt:

            raise ValueError(
                "User prompt cannot be empty."
            )


        # -------------------------------------------------
        # GROQ REQUEST
        # -------------------------------------------------

        try:

            response = (
                self.client
                .chat
                .completions
                .create(

                    model=self.model,

                    messages=[

                        {
                            "role": "system",

                            "content":
                                system_prompt
                        },

                        {
                            "role": "user",

                            "content":
                                user_prompt
                        }

                    ],

                    temperature=temperature,

                    max_tokens=max_tokens

                )
            )


            # -------------------------------------------------
            # EXTRACT RESPONSE
            # -------------------------------------------------

            if not response.choices:

                raise RuntimeError(
                    "Groq returned an empty response."
                )


            content = (
                response
                .choices[0]
                .message
                .content
            )


            if not content:

                raise RuntimeError(
                    "Groq returned empty message content."
                )


            return content.strip()


        except Exception as error:

            raise RuntimeError(
                f"Groq API request failed: {error}"
            ) from error


    # =====================================================
    # STREAM RESPONSE
    # =====================================================

    def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 3000
    ):

        # -------------------------------------------------
        # CONFIGURATION CHECK
        # -------------------------------------------------

        if not self.is_configured():

            raise RuntimeError(
                "GROQ_API_KEY is not configured."
            )


        # -------------------------------------------------
        # GROQ STREAM
        # -------------------------------------------------

        try:

            stream = (
                self.client
                .chat
                .completions
                .create(

                    model=self.model,

                    messages=[

                        {
                            "role": "system",
                            "content": system_prompt
                        },

                        {
                            "role": "user",
                            "content": user_prompt
                        }

                    ],

                    temperature=temperature,

                    max_tokens=max_tokens,

                    stream=True

                )
            )


            # -------------------------------------------------
            # RETURN EACH TOKEN
            # -------------------------------------------------

            for chunk in stream:

                if not chunk.choices:

                    continue


                content = (
                    chunk
                    .choices[0]
                    .delta
                    .content
                )


                if content:

                    yield content


        except Exception as error:

            raise RuntimeError(
                f"Groq streaming request failed: {error}"
            ) from error


# =========================================================
# SINGLETON
# =========================================================

_llm_client = None


def get_llm() -> LLMClient:

    global _llm_client


    if _llm_client is None:

        _llm_client = LLMClient()


    return _llm_client


# =========================================================
# SIMPLE GENERATE HELPER
# =========================================================

def generate_response(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 3000
) -> str:

    llm = get_llm()


    return llm.generate(

        system_prompt=system_prompt,

        user_prompt=user_prompt,

        temperature=temperature,

        max_tokens=max_tokens

    )


# =========================================================
# TEST GROQ CONNECTION
# =========================================================

def test_connection():

    llm = get_llm()


    print()
    print("=" * 65)
    print("              CHAOSPILOT GROQ TEST")
    print("=" * 65)

    print()

    print(
        f"Model: {llm.get_model()}"
    )

    print(
        f"API configured: "
        f"{llm.is_configured()}"
    )


    if not llm.is_configured():

        print()

        print(
            "❌ GROQ_API_KEY is not configured."
        )

        print(
            "Add your key to the .env file."
        )

        return


    print()

    print(
        "Sending test request..."
    )


    try:

        response = llm.generate(

            system_prompt=(
                "You are the ChaosPilot AI assistant. "
                "Reply briefly."
            ),

            user_prompt=(
                "Say exactly: "
                "ChaosPilot AI is online."
            ),

            temperature=0,

            max_tokens=50

        )


        print()

        print(
            "✅ Groq response:"
        )

        print(
            response
        )


    except Exception as error:

        print()

        print(
            "❌ Groq connection failed:"
        )

        print(
            error
        )


    print()

    print("=" * 65)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    test_connection()