"""Scratchpad Object."""

from __future__ import annotations

# Standard Python Libraries
import json
import re
import sys
from typing import Any

# Third-Party Libraries
from requests import exceptions as requests_exceptions
from requests.models import Response
from schema import And, Optional, Or, Regex, Schema, SchemaError

# Customer Libraries
from .abstract_endpoint import AbstractEndpoint

LANGUAGES = [
    "abap",
    "abc",
    "actionscript",
    "ada",
    "apache_conf",
    "asciidoc",
    "asl",
    "assembly_x86",
    "autohotkey",
    "sh",
    "batchfile",
    "bro",
    "c_cpp",
    "csharp",
    "c9search",
    "cirru",
    "clojure",
    "cobol",
    "coffee",
    "coldfusion",
    "csound_orchestra",
    "csound_document",
    "csound_score",
    "css",
    "curly",
    "d",
    "dart",
    "diff",
    "django",
    "dockerfile",
    "dot",
    "drools",
    "edifact",
    "eiffel",
    "ejs",
    "elixir",
    "elm",
    "erlang",
    "forth",
    "fortran",
    "ftl",
    "fsharp",
    "gcode",
    "gherkin",
    "gitignore",
    "glsl",
    "golang",
    "gobstones",
    "graphqlschema",
    "groovy",
    "haml",
    "handlebars",
    "haskell",
    "haskell_cabal",
    "haxe",
    "hjson",
    "html",
    "html_elixir",
    "html_ruby",
    "ini",
    "io",
    "jack",
    "jade",
    "java",
    "javascript",
    "json",
    "jsoniq",
    "jsp",
    "jssm",
    "jsx",
    "julia",
    "kotlin",
    "latex",
    "less",
    "liquid",
    "lisp",
    "livescript",
    "logiql",
    "lsl",
    "lua",
    "luapage",
    "lucene",
    "makefile",
    "markdown",
    "mask",
    "matlab",
    "maze",
    "mel",
    "mixal",
    "mushcode",
    "mysql",
    "nix",
    "nsis",
    "objectivec",
    "ocaml",
    "pascal",
    "perl",
    "pgsql",
    "php",
    "php_laravel_blade",
    "pig",
    "plain_text",
    "powershell",
    "praat",
    "prolog",
    "properties",
    "protobuf",
    "puppet",
    "python",
    "r",
    "razor",
    "rdoc",
    "red",
    "rhtml",
    "rst",
    "ruby",
    "rust",
    "sass",
    "scad",
    "scala",
    "scheme",
    "scss",
    "sh",
    "sjs",
    "slim",
    "smarty",
    "snippets",
    "soy_template",
    "space",
    "sql",
    "sqlserver",
    "stylus",
    "svg",
    "swift",
    "tcl",
    "terraform",
    "tex",
    "text",
    "textile",
    "toml",
    "tsx",
    "twig",
    "typescript",
    "vala",
    "vbscript",
    "velocity",
    "verilog",
    "vhdl",
    "wollok",
    "xml",
    "xquery",
]

TYPES = ["code", "rich"]


class Scratchpad(AbstractEndpoint):
    """Scratchpad Objects for Pentest.ws API.

    Attributes:
            id (str): The host id from pentest.ws
            hid (str): The host id that the port belongs to.
            title (str): The title of the scratchpad.
            type (str): The content type for the scratchpad, must match value from LANGUAGES.
            language (str): The language of the scratchpad content, must be "code" or "rich".
            content (str): The scratchpad's text content.

    """

    def __init__(self, **kwargs):
        """Initialize scratchpad object."""
        schema: Schema = Schema(
            {
                Optional("hid"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"hid" should be 8 alphanumeric characters',
                ),
                Optional("id"): And(
                    str,
                    Regex(r"^[a-zA-Z0-9]{8,}$", flags=re.IGNORECASE),
                    error='"id" should be 8 alphanumeric characters',
                ),
                "title": And(
                    str,
                    Regex(r"[a-zA-Z0-9]+", flags=re.IGNORECASE),
                    error='Scratchpad "title" is required.',
                ),
                Optional("type"): Or(
                    And(str, lambda submitted_type: submitted_type in TYPES),
                    And(None),
                    error=f'"type" should be None or one of the following: {str(TYPES)[1:-1]}',
                ),
                Optional("language"): Or(
                    And(
                        str, lambda submitted_language: submitted_language in LANGUAGES
                    ),
                    And(None),
                    error=f'"language" should be None or one of the following: {str(LANGUAGES)[1:-1]}',
                ),
                Optional("content"): Or(
                    str, None, error='"contented" should be a string or None.'
                ),
            }
        )

        try:
            validated_args: dict[str, Any] = schema.validate(kwargs)
        except SchemaError as err:
            # Raise error because 1 or more items were invalid.
            print(err, file=sys.stderr)
            raise

        for key, value in validated_args.items():
            setattr(self, key, value)

        try:
            # If a scratchpad ID is provided, creates the scratchpad_path.
            self.scratchpad_path: str = f"{AbstractEndpoint.path}/scratchpads/{self.id}"
        except AttributeError:
            pass

        if self.hid:
            # Create a new scratchpad or get the all scratchpads for host ID.
            self.host_path: str = (
                f"{AbstractEndpoint.path}/hosts/{self.hid}/scratchpads"
            )

    def create(self) -> str:
        """Create an Scratchpad in pentest.ws."""
        self.pws_session.headers["Content-Type"] = "application/json"

        scratchpad_dict: dict = self.to_dict()

        scratchpad_data: str = json.dumps(scratchpad_dict)

        # TODO Custom Exception (Issue 1)
        response: Response = self.pws_session.post(
            self.host_path, headers=self.pws_session.headers, data=scratchpad_data
        )

        # TODO Custom Exception (Issue 1)
        if response.status_code == 200:
            self.id = response.json()["id"]
            # FIXME The next line is flagged by mypy for Host not having an attribute "target".
            message: str = f"Scratchpad {self.title} ({self.id}) created."  # type: ignore
        elif response.status_code == 400:
            message = f"Error: {response.json()['msg']}"

        return message

    @staticmethod
    def get(id: str) -> Scratchpad:
        """Get a scratchpad from the API."""
        # TODO Custom Exception (Issue 1)
        try:
            response: Response = Scratchpad.pws_session.get(
                f"{AbstractEndpoint.path}/scratchpads/{id}"
            )
            response.raise_for_status()
        except requests_exceptions.HTTPError as err:
            raise SystemExit(err)
        else:
            return Scratchpad(**response.json())

    @staticmethod
    def get_all(hid: str) -> list[Scratchpad]:
        """Get all scratchpads from a Host."""
        # TODO Custom Exception (Issue 1)
        response: Response = Scratchpad.pws_session.get(
            f"{AbstractEndpoint.path}/hosts/{hid}/scratchpads"
        )
        scratchpads: list[Scratchpad] = list()

        for scratchpad_response in response.json():
            scratchpads.append(Scratchpad(**scratchpad_response))

        return scratchpads
