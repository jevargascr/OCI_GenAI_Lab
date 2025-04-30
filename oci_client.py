import oci

class OCIClient:
    def __init__(self, config_profile="DEFAULT", config_path="~/.oci/config", endpoint=None, compartment_id=None):
        self.config = oci.config.from_file(config_path, config_profile)
        self.endpoint = endpoint
        self.compartment_id = compartment_id
        self.client = oci.generative_ai_inference.GenerativeAiInferenceClient(
            config=self.config,
            service_endpoint=self.endpoint,
            retry_strategy=oci.retry.NoneRetryStrategy(),
            timeout=(10, 240)
        )

    def ask_question(self, prompt_text, model_id, temperature=1, max_tokens=600, top_p=0.75):
        content = oci.generative_ai_inference.models.TextContent(text=prompt_text)
        message = oci.generative_ai_inference.models.Message(role="USER", content=[content])

        chat_request = oci.generative_ai_inference.models.GenericChatRequest(
            api_format=oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=[message],
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=top_p
        )

        chat_detail = oci.generative_ai_inference.models.ChatDetails(
            serving_mode=oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id),
            compartment_id=self.compartment_id,
            chat_request=chat_request
        )

        response = self.client.chat(chat_detail)
        return response