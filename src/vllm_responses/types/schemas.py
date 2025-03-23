from collections.abc import Iterable
from typing import Dict, List, Literal, Optional, TypeAlias, Union

import pydantic

from vllm_responses.types.params import ResponseInputParam
from vllm_responses.types.reasoning import Reasoning
from vllm_responses.types.response import (
    IncompleteDetails,
    ResponseError,
    ResponseOutputItem,
    ResponseTextConfig,
    ResponseUsage,
    Tool,
)
from vllm_responses.types.response import ToolChoice as ToolChoice
from vllm_responses.types.tools import ToolParam


ResponseIncludable: TypeAlias = Literal[
    "file_search_call.results",
    "message.input_image.image_url",
    "computer_call_output.output.image_url",
]
Metadata: TypeAlias = Dict[str, str]


class ResponsesCreate(pydantic.BaseModel):
    """OpenAI Responses Create API Request Body."""

    input: Union[str, ResponseInputParam] = pydantic.Field(
        description="Text, image, or file inputs to the model, used to generate a response.",
    )
    model: str = pydantic.Field(
        description="Model ID used to generate the response.",
    )
    include: Optional[List[ResponseIncludable]] = pydantic.Field(
        default=None,
        description="Specify additional output data to include in the model response.",
    )
    instructions: Optional[str] = pydantic.Field(
        default=None,
        description="Inserts a system (or developer) message as the first item in the model's context.",
    )
    max_output_tokens: Optional[int] = pydantic.Field(
        default=None,
        description="An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.",
    )
    metadata: Optional[Metadata] = pydantic.Field(
        default=None,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.",
    )
    parallel_tool_calls: Optional[bool] = pydantic.Field(
        default=True,
        description="Whether to allow the model to run tool calls in parallel.",
    )
    previous_response_id: Optional[str] = pydantic.Field(
        default=None,
        description="The unique ID of the previous response to the model. Use this to create multi-turn conversations.",
    )
    reasoning: Optional[Reasoning] = pydantic.Field(
        default=None,
        description="Configuration options for reasoning models. **Reasoning models only**",
    )
    store: Optional[bool] = pydantic.Field(
        default=True,
        description="Whether to store the generated model response for later retrieval via API.",
    )
    stream: Optional[bool] = pydantic.Field(
        default=False,
        description="If set to true, the model response data will be streamed to the client as it is generated using server-sent events.",
    )
    temperature: Optional[float] = pydantic.Field(
        default=None,
        description="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.",
    )
    text: Optional[Dict[str, str]] = pydantic.Field(
        default=None,
        description="Configuration options for a text response from the model. Can be plain text or structured JSON data.",
    )
    tool_choice: Optional[ToolChoice] = pydantic.Field(
        default=None,
        description="How the model should select which tool (or tools) to use when generating a response. See the `tools` parameter to see how to specify which tools the model can call.",
    )
    tools: Optional[Iterable[ToolParam]] = pydantic.Field(
        default=None,
        description="An array of tools the model may call while generating a response. You can specify which tool to use by setting the `tool_choice` parameter.",
    )
    top_p: Optional[float] = pydantic.Field(
        default=1.0,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.",
    )
    truncation: Optional[Literal["auto", "disabled"]] = pydantic.Field(
        default="disabled",
        description="The truncation strategy to use for the model response.",
    )
    user: Optional[str] = pydantic.Field(
        default=None,
        description="A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.",
    )


class Response(pydantic.BaseModel):
    """OpenAI Responses Create API Response Body."""

    created_at: float = pydantic.Field(
        description="Unix timestamp (in seconds) of when this Response was created.",
    )
    error: Optional[ResponseError] = pydantic.Field(
        default=None,
        description="An error object returned when the model fails to generate a Response.",
    )
    id: str = pydantic.Field(
        description="Unique identifier for this Response.",
    )
    incomplete_details: Optional[IncompleteDetails] = pydantic.Field(
        default=None,
        description="Details about why the response is incomplete.",
    )
    instructions: Optional[str] = pydantic.Field(
        default=None,
        description="Inserts a system (or developer) message as the first item in the model's context.",
    )
    max_output_tokens: Optional[int] = pydantic.Field(
        default=None,
        description="An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.",
    )
    metadata: Optional[Metadata] = pydantic.Field(
        default=None,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.",
    )
    model: str = pydantic.Field(
        description="Model ID used to generate the response.",
    )
    object: Literal["response"] = pydantic.Field(
        description="The object type of this resource - always set to `response`.",
    )
    output: List[ResponseOutputItem] = pydantic.Field(
        description="An array of content items generated by the model.",
    )
    parallel_tool_calls: bool = pydantic.Field(
        description="Whether to allow the model to run tool calls in parallel.",
    )
    previous_response_id: Optional[str] = pydantic.Field(
        default=None,
        description="The unique ID of the previous response to the model. Use this to create multi-turn conversations.",
    )
    reasoning: Optional[Reasoning] = pydantic.Field(
        default=None,
        description="**o-series models only** Configuration options for [reasoning models](https://platform.openai.com/docs/guides/reasoning).",
    )
    status: Literal["completed", "failed", "in_progress", "incomplete"] = pydantic.Field(
        description="The status of the response generation.",
    )
    temperature: Optional[float] = pydantic.Field(
        default=None,
        description="What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.",
    )
    text: Optional[ResponseTextConfig] = pydantic.Field(
        default=None,
        description="Configuration options for a text response from the model. Can be plain text or structured JSON data.",
    )
    tool_choice: ToolChoice = pydantic.Field(
        description="How the model should select which tool (or tools) to use when generating a response. See the `tools` parameter to see how to specify which tools the model can call.",
    )
    tools: List[Tool] = pydantic.Field(
        description="An array of tools the model may call while generating a response. You can specify which tool to use by setting the `tool_choice` parameter.",
    )
    top_p: Optional[float] = pydantic.Field(
        default=None,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.",
    )
    truncation: Optional[Literal["auto", "disabled"]] = pydantic.Field(
        default="disabled",
        description="The truncation strategy to use for the model response.",
    )
    usage: Optional[ResponseUsage] = pydantic.Field(
        default=None,
        description="Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.",
    )
    user: Optional[str] = pydantic.Field(
        default=None,
        description="A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.",
    )
