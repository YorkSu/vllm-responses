from collections.abc import Iterable
from typing import Dict, List, Literal, Optional, TypeAlias, Union

from typing_extensions import Required, TypedDict


ToolChoiceOptions: TypeAlias = Literal["none", "auto", "required"]


class ToolChoiceFunctionParam(TypedDict, total=False):
    name: Required[str]
    """The name of the function to call."""

    type: Required[Literal["function"]]
    """For function calling, the type is always `function`."""


ToolChoice: TypeAlias = Union[ToolChoiceOptions, ToolChoiceFunctionParam]


class ComparisonFilter(TypedDict, total=False):
    key: Required[str]
    """The key to compare against the value."""

    type: Required[Literal["eq", "ne", "gt", "gte", "lt", "lte"]]
    """Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`.

    - `eq`: equals
    - `ne`: not equal
    - `gt`: greater than
    - `gte`: greater than or equal
    - `lt`: less than
    - `lte`: less than or equal
    """

    value: Required[Union[str, float, bool]]
    """
    The value to compare against the attribute key; supports string, number, or
    boolean types.
    """


class CompoundFilter(TypedDict, total=False):
    filters: Required[Iterable[Union[ComparisonFilter, object]]]
    """Array of filters to combine.

    Items can be `ComparisonFilter` or `CompoundFilter`.
    """

    type: Required[Literal["and", "or"]]
    """Type of operation: `and` or `or`."""


class RankingOptions(TypedDict, total=False):
    ranker: Literal["auto", "default-2024-11-15"]
    """The ranker to use for the file search."""

    score_threshold: float
    """
    The score threshold for the file search, a number between 0 and 1. Numbers
    closer to 1 will attempt to return only the most relevant results, but may
    return fewer results.
    """


class FileSearchToolParam(TypedDict, total=False):
    type: Required[Literal["file_search"]]
    """The type of the file search tool. Always `file_search`."""

    vector_store_ids: Required[List[str]]
    """The IDs of the vector stores to search."""

    filters: Union[ComparisonFilter, CompoundFilter]
    """A filter to apply based on file attributes."""

    max_num_results: int
    """The maximum number of results to return.

    This number should be between 1 and 50 inclusive.
    """

    ranking_options: RankingOptions
    """Ranking options for search."""


class FunctionToolParam(TypedDict, total=False):
    name: Required[str]
    """The name of the function to call."""

    parameters: Required[Dict[str, object]]
    """A JSON schema object describing the parameters of the function."""

    strict: Required[bool]
    """Whether to enforce strict parameter validation. Default `true`."""

    type: Required[Literal["function"]]
    """The type of the function tool. Always `function`."""

    description: Optional[str]
    """A description of the function.

    Used by the model to determine whether or not to call the function.
    """


class ComputerToolParam(TypedDict, total=False):
    display_height: Required[float]
    """The height of the computer display."""

    display_width: Required[float]
    """The width of the computer display."""

    environment: Required[Literal["mac", "windows", "ubuntu", "browser"]]
    """The type of computer environment to control."""

    type: Required[Literal["computer_use_preview"]]
    """The type of the computer use tool. Always `computer_use_preview`."""


class UserLocation(TypedDict, total=False):
    type: Required[Literal["approximate"]]
    """The type of location approximation. Always `approximate`."""

    city: str
    """Free text input for the city of the user, e.g. `San Francisco`."""

    country: str
    """
    The two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1) of
    the user, e.g. `US`.
    """

    region: str
    """Free text input for the region of the user, e.g. `California`."""

    timezone: str
    """
    The [IANA timezone](https://timeapi.io/documentation/iana-timezones) of the
    user, e.g. `America/Los_Angeles`.
    """


class WebSearchToolParam(TypedDict, total=False):
    type: Required[Literal["web_search_preview", "web_search_preview_2025_03_11"]]
    """The type of the web search tool. One of:

    - `web_search_preview`
    - `web_search_preview_2025_03_11`
    """

    search_context_size: Literal["low", "medium", "high"]
    """
    High level guidance for the amount of context window space to use for the
    search. One of `low`, `medium`, or `high`. `medium` is the default.
    """

    user_location: Optional[UserLocation]


ToolParam: TypeAlias = Union[FileSearchToolParam, FunctionToolParam, ComputerToolParam, WebSearchToolParam]
