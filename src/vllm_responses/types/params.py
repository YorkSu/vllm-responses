from collections.abc import Iterable
from typing import Dict, List, Literal, Optional, TypeAlias, Union

from typing_extensions import Required, TypedDict


class ResponseInputTextParam(TypedDict, total=False):
    text: Required[str]
    """The text input to the model."""

    type: Required[Literal["input_text"]]
    """The type of the input item. Always `input_text`."""


class ResponseInputImageParam(TypedDict, total=False):
    detail: Required[Literal["high", "low", "auto"]]
    """The detail level of the image to be sent to the model.

    One of `high`, `low`, or `auto`. Defaults to `auto`.
    """

    type: Required[Literal["input_image"]]
    """The type of the input item. Always `input_image`."""

    file_id: Optional[str]
    """The ID of the file to be sent to the model."""

    image_url: Optional[str]
    """The URL of the image to be sent to the model.

    A fully qualified URL or base64 encoded image in a data URL.
    """


class ResponseInputFileParam(TypedDict, total=False):
    type: Required[Literal["input_file"]]
    """The type of the input item. Always `input_file`."""

    file_data: str
    """The content of the file to be sent to the model."""

    file_id: str
    """The ID of the file to be sent to the model."""

    filename: str
    """The name of the file to be sent to the model."""


ResponseInputContentParam: TypeAlias = Union[ResponseInputTextParam, ResponseInputImageParam, ResponseInputFileParam]
ResponseInputMessageContentListParam: TypeAlias = List[ResponseInputContentParam]


class EasyInputMessageParam(TypedDict, total=False):
    content: Required[Union[str, ResponseInputMessageContentListParam]]
    """
    Text, image, or audio input to the model, used to generate a response. Can also
    contain previous assistant responses.
    """

    role: Required[Literal["user", "assistant", "system", "developer"]]
    """The role of the message input.

    One of `user`, `assistant`, `system`, or `developer`.
    """

    type: Literal["message"]
    """The type of the message input. Always `message`."""


class Message(TypedDict, total=False):
    content: Required[ResponseInputMessageContentListParam]
    """
    A list of one or many input items to the model, containing different content
    types.
    """

    role: Required[Literal["user", "system", "developer"]]
    """The role of the message input. One of `user`, `system`, or `developer`."""

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """

    type: Literal["message"]
    """The type of the message input. Always set to `message`."""


class AnnotationFileCitation(TypedDict, total=False):
    file_id: Required[str]
    """The ID of the file."""

    index: Required[int]
    """The index of the file in the list of files."""

    type: Required[Literal["file_citation"]]
    """The type of the file citation. Always `file_citation`."""


class AnnotationURLCitation(TypedDict, total=False):
    end_index: Required[int]
    """The index of the last character of the URL citation in the message."""

    start_index: Required[int]
    """The index of the first character of the URL citation in the message."""

    title: Required[str]
    """The title of the web resource."""

    type: Required[Literal["url_citation"]]
    """The type of the URL citation. Always `url_citation`."""

    url: Required[str]
    """The URL of the web resource."""


class AnnotationFilePath(TypedDict, total=False):
    file_id: Required[str]
    """The ID of the file."""

    index: Required[int]
    """The index of the file in the list of files."""

    type: Required[Literal["file_path"]]
    """The type of the file path. Always `file_path`."""


Annotation: TypeAlias = Union[AnnotationFileCitation, AnnotationURLCitation, AnnotationFilePath]


class ResponseOutputTextParam(TypedDict, total=False):
    annotations: Required[Iterable[Annotation]]
    """The annotations of the text output."""

    text: Required[str]
    """The text output from the model."""

    type: Required[Literal["output_text"]]
    """The type of the output text. Always `output_text`."""


class ResponseOutputRefusalParam(TypedDict, total=False):
    refusal: Required[str]
    """The refusal explanationfrom the model."""

    type: Required[Literal["refusal"]]
    """The type of the refusal. Always `refusal`."""


Content: TypeAlias = Union[ResponseOutputTextParam, ResponseOutputRefusalParam]


class ResponseOutputMessageParam(TypedDict, total=False):
    id: Required[str]
    """The unique ID of the output message."""

    content: Required[Iterable[Content]]
    """The content of the output message."""

    role: Required[Literal["assistant"]]
    """The role of the output message. Always `assistant`."""

    status: Required[Literal["in_progress", "completed", "incomplete"]]
    """The status of the message input.

    One of `in_progress`, `completed`, or `incomplete`. Populated when input items
    are returned via API.
    """

    type: Required[Literal["message"]]
    """The type of the output message. Always `message`."""


class Result(TypedDict, total=False):
    attributes: Optional[Dict[str, Union[str, float, bool]]]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format, and querying for objects via API or the dashboard. Keys are
    strings with a maximum length of 64 characters. Values are strings with a
    maximum length of 512 characters, booleans, or numbers.
    """

    file_id: str
    """The unique ID of the file."""

    filename: str
    """The name of the file."""

    score: float
    """The relevance score of the file - a value between 0 and 1."""

    text: str
    """The text that was retrieved from the file."""


class ResponseFileSearchToolCallParam(TypedDict, total=False):
    id: Required[str]
    """The unique ID of the file search tool call."""

    queries: Required[List[str]]
    """The queries used to search for files."""

    status: Required[Literal["in_progress", "searching", "completed", "incomplete", "failed"]]
    """The status of the file search tool call.

    One of `in_progress`, `searching`, `incomplete` or `failed`,
    """

    type: Required[Literal["file_search_call"]]
    """The type of the file search tool call. Always `file_search_call`."""

    results: Optional[Iterable[Result]]
    """The results of the file search tool call."""


class ActionClick(TypedDict, total=False):
    button: Required[Literal["left", "right", "wheel", "back", "forward"]]
    """Indicates which mouse button was pressed during the click.

    One of `left`, `right`, `wheel`, `back`, or `forward`.
    """

    type: Required[Literal["click"]]
    """Specifies the event type.

    For a click action, this property is always set to `click`.
    """

    x: Required[int]
    """The x-coordinate where the click occurred."""

    y: Required[int]
    """The y-coordinate where the click occurred."""


class ActionDoubleClick(TypedDict, total=False):
    type: Required[Literal["double_click"]]
    """Specifies the event type.

    For a double click action, this property is always set to `double_click`.
    """

    x: Required[int]
    """The x-coordinate where the double click occurred."""

    y: Required[int]
    """The y-coordinate where the double click occurred."""


class ActionDragPath(TypedDict, total=False):
    x: Required[int]
    """The x-coordinate."""

    y: Required[int]
    """The y-coordinate."""


class ActionDrag(TypedDict, total=False):
    path: Required[Iterable[ActionDragPath]]
    """An array of coordinates representing the path of the drag action.

    Coordinates will appear as an array of objects, eg

    ```
    [
      { x: 100, y: 200 },
      { x: 200, y: 300 }
    ]
    ```
    """

    type: Required[Literal["drag"]]
    """Specifies the event type.

    For a drag action, this property is always set to `drag`.
    """


class ActionKeypress(TypedDict, total=False):
    keys: Required[List[str]]
    """The combination of keys the model is requesting to be pressed.

    This is an array of strings, each representing a key.
    """

    type: Required[Literal["keypress"]]
    """Specifies the event type.

    For a keypress action, this property is always set to `keypress`.
    """


class ActionMove(TypedDict, total=False):
    type: Required[Literal["move"]]
    """Specifies the event type.

    For a move action, this property is always set to `move`.
    """

    x: Required[int]
    """The x-coordinate to move to."""

    y: Required[int]
    """The y-coordinate to move to."""


class ActionScreenshot(TypedDict, total=False):
    type: Required[Literal["screenshot"]]
    """Specifies the event type.

    For a screenshot action, this property is always set to `screenshot`.
    """


class ActionScroll(TypedDict, total=False):
    scroll_x: Required[int]
    """The horizontal scroll distance."""

    scroll_y: Required[int]
    """The vertical scroll distance."""

    type: Required[Literal["scroll"]]
    """Specifies the event type.

    For a scroll action, this property is always set to `scroll`.
    """

    x: Required[int]
    """The x-coordinate where the scroll occurred."""

    y: Required[int]
    """The y-coordinate where the scroll occurred."""


class ActionType(TypedDict, total=False):
    text: Required[str]
    """The text to type."""

    type: Required[Literal["type"]]
    """Specifies the event type.

    For a type action, this property is always set to `type`.
    """


class ActionWait(TypedDict, total=False):
    type: Required[Literal["wait"]]
    """Specifies the event type.

    For a wait action, this property is always set to `wait`.
    """


Action: TypeAlias = Union[
    ActionClick,
    ActionDoubleClick,
    ActionDrag,
    ActionKeypress,
    ActionMove,
    ActionScreenshot,
    ActionScroll,
    ActionType,
    ActionWait,
]


class PendingSafetyCheck(TypedDict, total=False):
    id: Required[str]
    """The ID of the pending safety check."""

    code: Required[str]
    """The type of the pending safety check."""

    message: Required[str]
    """Details about the pending safety check."""


class ResponseComputerToolCallParam(TypedDict, total=False):
    id: Required[str]
    """The unique ID of the computer call."""

    action: Required[Action]
    """A click action."""

    call_id: Required[str]
    """An identifier used when responding to the tool call with output."""

    pending_safety_checks: Required[Iterable[PendingSafetyCheck]]
    """The pending safety checks for the computer call."""

    status: Required[Literal["in_progress", "completed", "incomplete"]]
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """

    type: Required[Literal["computer_call"]]
    """The type of the computer call. Always `computer_call`."""


class ResponseComputerToolCallOutputScreenshotParam(TypedDict, total=False):
    type: Required[Literal["computer_screenshot"]]
    """Specifies the event type.

    For a computer screenshot, this property is always set to `computer_screenshot`.
    """

    file_id: str
    """The identifier of an uploaded file that contains the screenshot."""

    image_url: str
    """The URL of the screenshot image."""


class ComputerCallOutputAcknowledgedSafetyCheck(TypedDict, total=False):
    id: Required[str]
    """The ID of the pending safety check."""

    code: Required[str]
    """The type of the pending safety check."""

    message: Required[str]
    """Details about the pending safety check."""


class ComputerCallOutput(TypedDict, total=False):
    call_id: Required[str]
    """The ID of the computer tool call that produced the output."""

    output: Required[ResponseComputerToolCallOutputScreenshotParam]
    """A computer screenshot image used with the computer use tool."""

    type: Required[Literal["computer_call_output"]]
    """The type of the computer tool call output. Always `computer_call_output`."""

    id: str
    """The ID of the computer tool call output."""

    acknowledged_safety_checks: Iterable[ComputerCallOutputAcknowledgedSafetyCheck]
    """
    The safety checks reported by the API that have been acknowledged by the
    developer.
    """

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the message input.

    One of `in_progress`, `completed`, or `incomplete`. Populated when input items
    are returned via API.
    """


class ResponseFunctionWebSearchParam(TypedDict, total=False):
    id: Required[str]
    """The unique ID of the web search tool call."""

    status: Required[Literal["in_progress", "searching", "completed", "failed"]]
    """The status of the web search tool call."""

    type: Required[Literal["web_search_call"]]
    """The type of the web search tool call. Always `web_search_call`."""


class ResponseFunctionToolCallParam(TypedDict, total=False):
    arguments: Required[str]
    """A JSON string of the arguments to pass to the function."""

    call_id: Required[str]
    """The unique ID of the function tool call generated by the model."""

    name: Required[str]
    """The name of the function to run."""

    type: Required[Literal["function_call"]]
    """The type of the function tool call. Always `function_call`."""

    id: str
    """The unique ID of the function tool call."""

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """


class FunctionCallOutput(TypedDict, total=False):
    call_id: Required[str]
    """The unique ID of the function tool call generated by the model."""

    output: Required[str]
    """A JSON string of the output of the function tool call."""

    type: Required[Literal["function_call_output"]]
    """The type of the function tool call output. Always `function_call_output`."""

    id: str
    """The unique ID of the function tool call output.

    Populated when this item is returned via API.
    """

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """


class Summary(TypedDict, total=False):
    text: Required[str]
    """
    A short summary of the reasoning used by the model when generating the response.
    """

    type: Required[Literal["summary_text"]]
    """The type of the object. Always `summary_text`."""


class ResponseReasoningItemParam(TypedDict, total=False):
    id: Required[str]
    """The unique identifier of the reasoning content."""

    summary: Required[Iterable[Summary]]
    """Reasoning text contents."""

    type: Required[Literal["reasoning"]]
    """The type of the object. Always `reasoning`."""

    status: Literal["in_progress", "completed", "incomplete"]
    """The status of the item.

    One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
    """


class ItemReference(TypedDict, total=False):
    id: Required[str]
    """The ID of the item to reference."""

    type: Required[Literal["item_reference"]]
    """The type of item to reference. Always `item_reference`."""


ResponseInputItemParam: TypeAlias = Union[
    EasyInputMessageParam,
    Message,
    ResponseOutputMessageParam,
    ResponseFileSearchToolCallParam,
    ResponseComputerToolCallParam,
    ComputerCallOutput,
    ResponseFunctionWebSearchParam,
    ResponseFunctionToolCallParam,
    FunctionCallOutput,
    ResponseReasoningItemParam,
    ItemReference,
]
ResponseInputParam: TypeAlias = List[ResponseInputItemParam]
