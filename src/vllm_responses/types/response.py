from typing import Dict, List, Literal, Optional, TypeAlias, Union

import pydantic
from typing_extensions import Annotated

from vllm_responses.types.tools import ToolChoiceOptions
from vllm_responses.types.transform import PropertyInfo


class ResponseError(pydantic.BaseModel):
    code: Literal[
        "server_error",
        "rate_limit_exceeded",
        "invalid_prompt",
        "vector_store_timeout",
        "invalid_image",
        "invalid_image_format",
        "invalid_base64_image",
        "invalid_image_url",
        "image_too_large",
        "image_too_small",
        "image_parse_error",
        "image_content_policy_violation",
        "invalid_image_mode",
        "image_file_too_large",
        "unsupported_image_media_type",
        "empty_image_file",
        "failed_to_download_image",
        "image_file_not_found",
    ]
    """The error code for the response."""

    message: str
    """A human-readable description of the error."""


class IncompleteDetails(pydantic.BaseModel):
    reason: Optional[Literal["max_output_tokens", "content_filter"]] = None
    """The reason why the response is incomplete."""


class AnnotationFileCitation(pydantic.BaseModel):
    file_id: str
    """The ID of the file."""

    index: int
    """The index of the file in the list of files."""

    type: Literal["file_citation"]
    """The type of the file citation. Always `file_citation`."""


class AnnotationURLCitation(pydantic.BaseModel):
    end_index: int
    """The index of the last character of the URL citation in the message."""

    start_index: int
    """The index of the first character of the URL citation in the message."""

    title: str
    """The title of the web resource."""

    type: Literal["url_citation"]
    """The type of the URL citation. Always `url_citation`."""

    url: str
    """The URL of the web resource."""


class AnnotationFilePath(pydantic.BaseModel):
    file_id: str
    """The ID of the file."""

    index: int
    """The index of the file in the list of files."""

    type: Literal["file_path"]
    """The type of the file path. Always `file_path`."""


Annotation: TypeAlias = Annotated[
    Union[AnnotationFileCitation, AnnotationURLCitation, AnnotationFilePath], PropertyInfo(discriminator="type")
]


class ResponseOutputText(pydantic.BaseModel):
    annotations: List[Annotation]
    """The annotations of the text output."""

    text: str
    """The text output from the model."""

    type: Literal["output_text"]
    """The type of the output text. Always `output_text`."""


class ResponseOutputRefusal(pydantic.BaseModel):
    refusal: str
    """The refusal explanationfrom the model."""

    type: Literal["refusal"]
    """The type of the refusal. Always `refusal`."""


Content: TypeAlias = Annotated[Union[ResponseOutputText, ResponseOutputRefusal], PropertyInfo(discriminator="type")]


class ResponseOutputMessage(pydantic.BaseModel):
    id: str
    """The unique ID of the output message."""

    content: List[Content]
    """The content of the output message."""

    role: Literal["assistant"]
    """The role of the output message. Always `assistant`."""

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the message input.

    One of `in_progress`, `completed`, or `incomplete`. Populated when input items
    are returned via API.
    """

    type: Literal["message"]
    """The type of the output message. Always `message`."""


class Result(pydantic.BaseModel):
    attributes: Optional[Dict[str, Union[str, float, bool]]] = None
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format, and querying for objects via API or the dashboard. Keys are
    strings with a maximum length of 64 characters. Values are strings with a
    maximum length of 512 characters, booleans, or numbers.
    """

    file_id: Optional[str] = None
    """The unique ID of the file."""

    filename: Optional[str] = None
    """The name of the file."""

    score: Optional[float] = None
    """The relevance score of the file - a value between 0 and 1."""

    text: Optional[str] = None
    """The text that was retrieved from the file."""


class ResponseFileSearchToolCall(pydantic.BaseModel):
    id: str
    """The unique ID of the file search tool call."""

    queries: List[str]
    """The queries used to search for files."""

    status: Literal["in_progress", "searching", "completed", "incomplete", "failed"]
    """The status of the file search tool call.

    One of `in_progress`, `searching`, `incomplete` or `failed`,
    """

    type: Literal["file_search_call"]
    """The type of the file search tool call. Always `file_search_call`."""

    results: Optional[List[Result]] = None
    """The results of the file search tool call."""


class ResponseFunctionToolCall(pydantic.BaseModel):
    arguments: str
    """A JSON string of the arguments to pass to the function."""

    call_id: str
    """The unique ID of the function tool call generated by the model."""

    name: str
    """The name of the function to run."""

    type: Literal["function_call"]
    """The type of the function tool call. Always `function_call`."""

    id: Optional[str] = None
    """The unique ID of the function tool call."""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """


class ResponseFunctionWebSearch(pydantic.BaseModel):
    id: str
    """The unique ID of the web search tool call."""

    status: Literal["in_progress", "searching", "completed", "failed"]
    """The status of the web search tool call."""

    type: Literal["web_search_call"]
    """The type of the web search tool call. Always `web_search_call`."""


class ActionClick(pydantic.BaseModel):
    button: Literal["left", "right", "wheel", "back", "forward"]
    """Indicates which mouse button was pressed during the click.

    One of `left`, `right`, `wheel`, `back`, or `forward`.
    """

    type: Literal["click"]
    """Specifies the event type.

    For a click action, this property is always set to `click`.
    """

    x: int
    """The x-coordinate where the click occurred."""

    y: int
    """The y-coordinate where the click occurred."""


class ActionDoubleClick(pydantic.BaseModel):
    type: Literal["double_click"]
    """Specifies the event type.

    For a double click action, this property is always set to `double_click`.
    """

    x: int
    """The x-coordinate where the double click occurred."""

    y: int
    """The y-coordinate where the double click occurred."""


class ActionDragPath(pydantic.BaseModel):
    x: int
    """The x-coordinate."""

    y: int
    """The y-coordinate."""


class ActionDrag(pydantic.BaseModel):
    path: List[ActionDragPath]
    """An array of coordinates representing the path of the drag action.

    Coordinates will appear as an array of objects, eg

    ```
    [
      { x: 100, y: 200 },
      { x: 200, y: 300 }
    ]
    ```
    """

    type: Literal["drag"]
    """Specifies the event type.

    For a drag action, this property is always set to `drag`.
    """


class ActionKeypress(pydantic.BaseModel):
    keys: List[str]
    """The combination of keys the model is requesting to be pressed.

    This is an array of strings, each representing a key.
    """

    type: Literal["keypress"]
    """Specifies the event type.

    For a keypress action, this property is always set to `keypress`.
    """


class ActionMove(pydantic.BaseModel):
    type: Literal["move"]
    """Specifies the event type.

    For a move action, this property is always set to `move`.
    """

    x: int
    """The x-coordinate to move to."""

    y: int
    """The y-coordinate to move to."""


class ActionScreenshot(pydantic.BaseModel):
    type: Literal["screenshot"]
    """Specifies the event type.

    For a screenshot action, this property is always set to `screenshot`.
    """


class ActionScroll(pydantic.BaseModel):
    scroll_x: int
    """The horizontal scroll distance."""

    scroll_y: int
    """The vertical scroll distance."""

    type: Literal["scroll"]
    """Specifies the event type.

    For a scroll action, this property is always set to `scroll`.
    """

    x: int
    """The x-coordinate where the scroll occurred."""

    y: int
    """The y-coordinate where the scroll occurred."""


class ActionType(pydantic.BaseModel):
    text: str
    """The text to type."""

    type: Literal["type"]
    """Specifies the event type.

    For a type action, this property is always set to `type`.
    """


class ActionWait(pydantic.BaseModel):
    type: Literal["wait"]
    """Specifies the event type.

    For a wait action, this property is always set to `wait`.
    """


Action: TypeAlias = Annotated[
    Union[
        ActionClick,
        ActionDoubleClick,
        ActionDrag,
        ActionKeypress,
        ActionMove,
        ActionScreenshot,
        ActionScroll,
        ActionType,
        ActionWait,
    ],
    PropertyInfo(discriminator="type"),
]


class PendingSafetyCheck(pydantic.BaseModel):
    id: str
    """The ID of the pending safety check."""

    code: str
    """The type of the pending safety check."""

    message: str
    """Details about the pending safety check."""


class ResponseComputerToolCall(pydantic.BaseModel):
    id: str
    """The unique ID of the computer call."""

    action: Action
    """A click action."""

    call_id: str
    """An identifier used when responding to the tool call with output."""

    pending_safety_checks: List[PendingSafetyCheck]
    """The pending safety checks for the computer call."""

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """

    type: Literal["computer_call"]
    """The type of the computer call. Always `computer_call`."""


class Summary(pydantic.BaseModel):
    text: str
    """
    A short summary of the reasoning used by the model when generating the response.
    """

    type: Literal["summary_text"]
    """The type of the object. Always `summary_text`."""


class ResponseReasoningItem(pydantic.BaseModel):
    id: str
    """The unique identifier of the reasoning content."""

    summary: List[Summary]
    """Reasoning text contents."""

    type: Literal["reasoning"]
    """The type of the object. Always `reasoning`."""

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """


ResponseOutputItem: TypeAlias = Annotated[
    Union[
        ResponseOutputMessage,
        ResponseFileSearchToolCall,
        ResponseFunctionToolCall,
        ResponseFunctionWebSearch,
        ResponseComputerToolCall,
        ResponseReasoningItem,
    ],
    PropertyInfo(discriminator="type"),
]


class ToolChoiceFunction(pydantic.BaseModel):
    name: str
    """The name of the function to call."""

    type: Literal["function"]
    """For function calling, the type is always `function`."""


ToolChoice: TypeAlias = Union[ToolChoiceOptions, ToolChoiceFunction]


class ComparisonFilter(pydantic.BaseModel):
    key: str
    """The key to compare against the value."""

    type: Literal["eq", "ne", "gt", "gte", "lt", "lte"]
    """Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`.

    - `eq`: equals
    - `ne`: not equal
    - `gt`: greater than
    - `gte`: greater than or equal
    - `lt`: less than
    - `lte`: less than or equal
    """

    value: Union[str, float, bool]
    """
    The value to compare against the attribute key; supports string, number, or
    boolean types.
    """


class CompoundFilter(pydantic.BaseModel):
    filters: List[Union[ComparisonFilter, object]]
    """Array of filters to combine.

    Items can be `ComparisonFilter` or `CompoundFilter`.
    """

    type: Literal["and", "or"]
    """Type of operation: `and` or `or`."""


class RankingOptions(pydantic.BaseModel):
    ranker: Optional[Literal["auto", "default-2024-11-15"]] = None
    """The ranker to use for the file search."""

    score_threshold: Optional[float] = None
    """
    The score threshold for the file search, a number between 0 and 1. Numbers
    closer to 1 will attempt to return only the most relevant results, but may
    return fewer results.
    """


class FileSearchTool(pydantic.BaseModel):
    type: Literal["file_search"]
    """The type of the file search tool. Always `file_search`."""

    vector_store_ids: List[str]
    """The IDs of the vector stores to search."""

    filters: Optional[Union[ComparisonFilter, CompoundFilter]] = None
    """A filter to apply based on file attributes."""

    max_num_results: Optional[int] = None
    """The maximum number of results to return.

    This number should be between 1 and 50 inclusive.
    """

    ranking_options: Optional[RankingOptions] = None
    """Ranking options for search."""


class FunctionTool(pydantic.BaseModel):
    name: str
    """The name of the function to call."""

    parameters: Dict[str, object]
    """A JSON schema object describing the parameters of the function."""

    strict: bool
    """Whether to enforce strict parameter validation. Default `true`."""

    type: Literal["function"]
    """The type of the function tool. Always `function`."""

    description: Optional[str] = None
    """A description of the function.

    Used by the model to determine whether or not to call the function.
    """


class ComputerTool(pydantic.BaseModel):
    display_height: float
    """The height of the computer display."""

    display_width: float
    """The width of the computer display."""

    environment: Literal["mac", "windows", "ubuntu", "browser"]
    """The type of computer environment to control."""

    type: Literal["computer_use_preview"]
    """The type of the computer use tool. Always `computer_use_preview`."""


class UserLocation(pydantic.BaseModel):
    type: Literal["approximate"]
    """The type of location approximation. Always `approximate`."""

    city: Optional[str] = None
    """Free text input for the city of the user, e.g. `San Francisco`."""

    country: Optional[str] = None
    """
    The two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1) of
    the user, e.g. `US`.
    """

    region: Optional[str] = None
    """Free text input for the region of the user, e.g. `California`."""

    timezone: Optional[str] = None
    """
    The [IANA timezone](https://timeapi.io/documentation/iana-timezones) of the
    user, e.g. `America/Los_Angeles`.
    """


class WebSearchTool(pydantic.BaseModel):
    type: Literal["web_search_preview", "web_search_preview_2025_03_11"]
    """The type of the web search tool. One of:

    - `web_search_preview`
    - `web_search_preview_2025_03_11`
    """

    search_context_size: Optional[Literal["low", "medium", "high"]] = None
    """
    High level guidance for the amount of context window space to use for the
    search. One of `low`, `medium`, or `high`. `medium` is the default.
    """

    user_location: Optional[UserLocation] = None


Tool: TypeAlias = Annotated[
    Union[FileSearchTool, FunctionTool, ComputerTool, WebSearchTool], PropertyInfo(discriminator="type")
]


ReasoningEffort: TypeAlias = Optional[Literal["low", "medium", "high"]]


class Reasoning(pydantic.BaseModel):
    effort: Optional[ReasoningEffort] = None
    """**o-series models only**

    Constrains effort on reasoning for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
    supported values are `low`, `medium`, and `high`. Reducing reasoning effort can
    result in faster responses and fewer tokens used on reasoning in a response.
    """

    generate_summary: Optional[Literal["concise", "detailed"]] = None
    """**computer_use_preview only**

    A summary of the reasoning performed by the model. This can be useful for
    debugging and understanding the model's reasoning process. One of `concise` or
    `detailed`.
    """


class ResponseFormatText(pydantic.BaseModel):
    type: Literal["text"]
    """The type of response format being defined. Always `text`."""


class ResponseFormatTextJSONSchemaConfig(pydantic.BaseModel):
    schema_: Dict[str, object] = pydantic.Field(alias="schema")
    """
    The schema for the response format, described as a JSON Schema object. Learn how
    to build JSON schemas [here](https://json-schema.org/).
    """

    type: Literal["json_schema"]
    """The type of response format being defined. Always `json_schema`."""

    description: Optional[str] = None
    """
    A description of what the response format is for, used by the model to determine
    how to respond in the format.
    """

    name: Optional[str] = None
    """The name of the response format.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    strict: Optional[bool] = None
    """
    Whether to enable strict schema adherence when generating the output. If set to
    true, the model will always follow the exact schema defined in the `schema`
    field. Only a subset of JSON Schema is supported when `strict` is `true`. To
    learn more, read the
    [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
    """


class ResponseFormatJSONObject(pydantic.BaseModel):
    type: Literal["json_object"]
    """The type of response format being defined. Always `json_object`."""


ResponseFormatTextConfig: TypeAlias = Annotated[
    Union[ResponseFormatText, ResponseFormatTextJSONSchemaConfig, ResponseFormatJSONObject],
    PropertyInfo(discriminator="type"),
]


class ResponseTextConfig(pydantic.BaseModel):
    format: Optional[ResponseFormatTextConfig] = None
    """An object specifying the format that the model must output.

    Configuring `{ "type": "json_schema" }` enables Structured Outputs, which
    ensures the model will match your supplied JSON schema. Learn more in the
    [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).

    The default format is `{ "type": "text" }` with no additional options.

    **Not recommended for gpt-4o and newer models:**

    Setting to `{ "type": "json_object" }` enables the older JSON mode, which
    ensures the message the model generates is valid JSON. Using `json_schema` is
    preferred for models that support it.
    """


class InputTokensDetails(pydantic.BaseModel):
    cached_tokens: int
    """The number of tokens that were retrieved from the cache.

    [More on prompt caching](https://platform.openai.com/docs/guides/prompt-caching).
    """


class OutputTokensDetails(pydantic.BaseModel):
    reasoning_tokens: int
    """The number of reasoning tokens."""


class ResponseUsage(pydantic.BaseModel):
    input_tokens: int
    """The number of input tokens."""

    input_tokens_details: InputTokensDetails
    """A detailed breakdown of the input tokens."""

    output_tokens: int
    """The number of output tokens."""

    output_tokens_details: OutputTokensDetails
    """A detailed breakdown of the output tokens."""

    total_tokens: int
    """The total number of tokens used."""
