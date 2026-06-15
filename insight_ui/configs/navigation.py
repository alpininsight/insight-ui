"""Configuration classes for navigation components."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import HtmxConfig, IconConfig
from insight_ui.configs.input import DropdownConfig
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import BrandLockupConfig, CopyrightNoticeConfig, LogoConfig


@dataclass
class NavbarBrandConfig:
    """
    Configuration for the navbar brand section.

    Describes the title and the logo of the application in the navbar.

    Attributes:
        title: The title of the application.
        request_url: Name of the URL to be called when clicking on the title.
        logo: Describes the logo that is displayed next to the title.
        gap: This value determines the spacing between the logo and the title.
        aria_label: Optional accessible label for the brand link.
        lockup: Optional controlled brand lockup rendered instead of logo plus title.

    """

    __example__ = """
        NavbarBrandConfig(
            title="My App",
            request_url=reverse("index"),
            logo=LogoConfig(url="img/logo.svg", height="2rem"),
        )
        """

    title: str = field(default="", metadata={"doc": _("The title of the application.")})
    request_url: str = field(
        default="", metadata={"doc": _("Name of the URL to be called when clicking on the title.")}
    )
    logo: LogoConfig | None = field(
        default=None, metadata={"doc": _("Describes the logo that is displayed next to the title.")}
    )
    gap: str = field(
        default="0.5rem", metadata={"doc": _("This value determines the spacing between the logo and the title.")}
    )
    aria_label: str = field(default="", metadata={"doc": _("Optional accessible label for the brand link.")})
    lockup: BrandLockupConfig | None = field(
        default=None, metadata={"doc": _("Optional controlled brand lockup rendered instead of logo plus title.")}
    )


@dataclass
class NavbarLinkConfig:
    """
    Configuration for a navbar navigation link.

    Attributes:
        text: Label of the link.
        url: The URL to be called when clicking on the link, if not opening a modal or dropdown menu.
        icon: An optional icon displayed before the text.
        need_auth: The link is only displayed for logged-in users.
        staff_only: The link is only displayed for administrators.
        modal: Configuration of a modal dialog.
        dropdown: Configuration of a dropdown menu.

    """

    __example__ = """
        NavbarLinkConfig(text="Home", url=reverse("index"))
        """

    text: str = field(metadata={"doc": _("Label of the link.")})
    url: str = field(
        default="",
        metadata={"doc": _("The URL to be called when clicking on the link, if not opening a modal or dropdown menu.")},
    )
    icon: IconConfig | None = field(default=None, metadata={"doc": _("An optional icon displayed before the text.")})
    need_auth: bool = field(default=False, metadata={"doc": _("The link is only displayed for logged-in users.")})
    staff_only: bool = field(default=False, metadata={"doc": _("The link is only displayed for administrators.")})
    modal: ModalConfig | None = field(default=None, metadata={"doc": _("Configuration of a modal dialog.")})
    dropdown: DropdownConfig | None = field(default=None, metadata={"doc": _("Configuration of a dropdown menu.")})


@dataclass
class NavbarConfig:
    """
    Configuration for the navbar component.

    Renders a full navigation bar with brand, links, and optional features.

    Attributes:
        brand: Describes the title and the logo of the application in the navbar.
        links: Contains and describes the navigation items of the navbar.
        searchbar_request_url: The URL to be called when performing a search. If empty, no search bar will be displayed.
        show_usermenu: Displays a dropdown menu with at least a logout button.
        show_language_selector: Displays a dropdown menu for selecting the display language (if defined).
        show_theme_toggle: Displays a button to switch between the light and dark theme of the page.

    """

    __example__ = """
        NavbarConfig(
            brand=NavbarBrandConfig(
                title="My App",
                request_url=reverse("index"),
                logo=LogoConfig(url="img/logo.svg", height="2rem"),
            ),
            links=[
                NavbarLinkConfig(text="Home", url=reverse("index")),
                NavbarLinkConfig(text="About", url=reverse("about")),
                NavbarLinkConfig(text="Admin", url=reverse("admin:index"), staff_only=True),
            ],
            show_usermenu=True,
            show_theme_toggle=True,
        )
        """

    brand: NavbarBrandConfig | None = field(
        default=None, metadata={"doc": _("Describes the title and the logo of the application in the navbar.")}
    )
    links: list[NavbarLinkConfig] = field(
        default_factory=list, metadata={"doc": _("Contains and describes the navigation items of the navbar.")}
    )
    searchbar_request_url: str = field(
        default="",
        metadata={
            "doc": _("The URL to be called when performing a search. If empty, no search bar will be displayed.")
        },
    )
    show_usermenu: bool = field(
        default=False, metadata={"doc": _("Displays a dropdown menu with at least a logout button.")}
    )
    show_language_selector: bool = field(
        default=False, metadata={"doc": _("Displays a dropdown menu for selecting the display language (if defined).")}
    )
    show_theme_toggle: bool = field(
        default=False, metadata={"doc": _("Displays a button to switch between the light and dark theme of the page.")}
    )


@dataclass
class SidebarItemConfig:
    """
    Configuration for a sidebar navigation item.

    Attributes:
        text: Label of the item.
        request_url: The URL to be called when clicking on the item.
        icon: An optional icon displayed before the text.
        htmx: HTMX configuration for AJAX page changes.
        url: Backwards-compatible alias for dictionary-based sidebar items.

    """

    __example__ = """
        SidebarItemConfig(text="Profile", request_url=reverse("profile"))
        """

    text: str = field(metadata={"doc": _("Label of the item.")})
    request_url: str = field(default="", metadata={"doc": _("The URL to be called when clicking on the item.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("An optional icon displayed before the text.")})
    htmx: HtmxConfig | None = field(default=None, metadata={"doc": _("HTMX configuration for AJAX page changes.")})
    url: str = field(default="", metadata={"doc": _("Backwards-compatible alias for dictionary-based sidebar items.")})


@dataclass
class SidebarCategoryConfig:
    """
    Configuration for a sidebar category (group of items).

    Attributes:
        caption: Category header text.
        icon: Optional category icon.
        items: List of items in this category.
        collapsed: Whether category is initially collapsed.

    """

    __example__ = """
        SidebarCategoryConfig(
            caption="Account",
            items=[
                SidebarItemConfig(text="Profile", request_url=reverse("profile")),
                SidebarItemConfig(text="Security", request_url=reverse("security")),
            ],
        )
        """

    caption: str = field(metadata={"doc": _("Category header text.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional category icon.")})
    items: list[SidebarItemConfig] = field(default_factory=list, metadata={"doc": _("List of items in this category.")})
    collapsed: bool = field(default=False, metadata={"doc": _("Whether category is initially collapsed.")})


@dataclass
class SidebarDataConfig:
    """
    Configuration for sidebar content.

    Attributes:
        title: Sidebar title.
        icon: Optional title icon.
        categories: List of navigation categories.

    """

    __example__ = """
        SidebarDataConfig(
            title="Settings",
            categories=[
                SidebarCategoryConfig(
                    caption="Account",
                    items=[
                        SidebarItemConfig(text="Profile", request_url=reverse("profile")),
                        SidebarItemConfig(text="Security", request_url=reverse("security")),
                    ],
                ),
            ],
        )
        """

    title: str = field(default="", metadata={"doc": _("Sidebar title.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional title icon.")})
    categories: list[SidebarCategoryConfig] = field(
        default_factory=list, metadata={"doc": _("List of navigation categories.")}
    )


@dataclass
class SidebarConfig:
    """
    Configuration for the sidebar component.

    Renders a side navigation panel.

    Attributes:
        sidebar_data: Content of the sidebar (title and navigation elements).
        side: Determines on which side the sidebar should be placed.
        static: **True** if the sidebar should not be collapsible.
        auto_close: If **True** the sidebar closes as soon as the cursor leaves it.
        mobile_hidden: If **True** the static sidebar is hidden on a smaller viewport.

    """

    __example__ = """
        SidebarConfig(
            sidebar_data=SidebarDataConfig(
                title="Settings",
                categories=[
                    SidebarCategoryConfig(
                        caption="Account",
                        items=[
                            SidebarItemConfig(text="Profile", request_url=reverse("profile")),
                            SidebarItemConfig(text="Security", request_url=reverse("security")),
                        ],
                    ),
                ],
            ),
            side="left",
            static=True,
        )
        """

    sidebar_data: SidebarDataConfig | None = field(
        default=None, metadata={"doc": _("Content of the sidebar (title and navigation elements).")}
    )
    side: Literal["left", "right"] = field(
        default="right", metadata={"doc": _("Determines on which side the sidebar should be placed.")}
    )
    static: bool = field(default=True, metadata={"doc": _("**True** if the sidebar should not be collapsible.")})
    auto_close: bool = field(
        default=False, metadata={"doc": _("If **True** the sidebar closes as soon as the cursor leaves it.")}
    )
    mobile_hidden: bool = field(
        default=False, metadata={"doc": _("If **True** the static sidebar is hidden on a smaller viewport.")}
    )


@dataclass
class FooterDescriptionConfig:
    """
    Configuration for the footer description section.

    Brief description of the application with optional image.

    Attributes:
        title: Heading of the description.
        text: Brief summary of the application.
        logo: Optional image displayed below the description text.

    """

    __example__ = """
        FooterDescriptionConfig(
            title="My App",
            text="A modern web application.",
        )
        """

    title: str = field(default="", metadata={"doc": _("Heading of the description.")})
    text: str = field(default="", metadata={"doc": _("Brief summary of the application.")})
    logo: LogoConfig | None = field(
        default=None, metadata={"doc": _("Optional image displayed below the description text.")}
    )


@dataclass
class FooterContactConfig:
    """
    Configuration for footer contact information.

    Contact information, link to the imprint, privacy policy and a contact email address.

    Attributes:
        mail_url: URL of a contact email address.
        imprint: Link to an imprint.
        privacy: Link to a privacy policy.

    """

    __example__ = """
        FooterContactConfig(
            mail_url="support@example.com",
            imprint="/imprint/",
            privacy="/privacy/",
        )
        """

    mail_url: str = field(default="", metadata={"doc": _("URL of a contact email address.")})
    imprint: str = field(default="", metadata={"doc": _("Link to an imprint.")})
    privacy: str = field(default="", metadata={"doc": _("Link to a privacy policy.")})


@dataclass
class FooterConfig:
    """
    Configuration for the footer component.

    Renders a complete page footer.

    Attributes:
        description: Brief description of the application with optional image.
        links: List of the main navigation items of the application.
        contact: Contact information, link to the imprint, privacy policy and a contact email address.
        copyright: Copyright information, such as the year, holder, source label, and license text.
        version: Information about the current version.

    """

    __example__ = """
        FooterConfig(
            description=FooterDescriptionConfig(
                title="My App",
                text="A modern web application.",
            ),
            links=[
                NavbarLinkConfig(text="Home", url=reverse("index")),
                NavbarLinkConfig(text="Docs", url="https://docs.example.com"),
            ],
            contact=FooterContactConfig(
                mail_url="support@example.com",
                imprint="/imprint/",
                privacy="/privacy/",
            ),
            copyright=CopyrightNoticeConfig(
                year=2026,
                holder="My Company",
            ),
            version="v1.0.0",
        )
        """

    description: FooterDescriptionConfig | None = field(
        default=None, metadata={"doc": _("Brief description of the application with optional image.")}
    )
    links: list[NavbarLinkConfig] = field(
        default_factory=list, metadata={"doc": _("List of the main navigation items of the application.")}
    )
    contact: FooterContactConfig | None = field(
        default=None,
        metadata={"doc": _("Contact information, link to the imprint, privacy policy and a contact email address.")},
    )
    copyright: CopyrightNoticeConfig | None = field(
        default=None,
        metadata={"doc": _("Copyright information, such as the year, holder, source label, and license text.")},
    )
    version: str = field(default="", metadata={"doc": _("Information about the current version.")})


@dataclass
class BreadcrumbItemConfig:
    """
    Configuration for a breadcrumb navigation item.

    Attributes:
        text: Label of the link.
        request_url: The URL to be called when clicking on the link.
        icon: Optional icon (typically for home item).

    """

    __example__ = """
        BreadcrumbItemConfig(text="Home", request_url="/", icon=IconConfig("home"))
        """

    text: str = field(metadata={"doc": _("Label of the link.")})
    request_url: str = field(default="", metadata={"doc": _("The URL to be called when clicking on the link.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Optional icon (typically for home item).")})


@dataclass
class BreadcrumbsConfig:
    """
    Configuration for the breadcrumbs component.

    Renders a breadcrumb navigation trail.

    Attributes:
        items: List of breadcrumb navigation items.
        htmx: Optional HTMX configuration for AJAX navigation.

    """

    __example__ = """
        BreadcrumbsConfig(
            items=[
                BreadcrumbItemConfig(text="Home", request_url="/", icon=IconConfig("home")),
                BreadcrumbItemConfig(text="Products", request_url="/products/"),
                BreadcrumbItemConfig(text="Laptops"),
            ],
        )
        """

    items: list[BreadcrumbItemConfig] = field(
        default_factory=list, metadata={"doc": _("List of breadcrumb navigation items.")}
    )
    htmx: HtmxConfig | None = field(
        default=None, metadata={"doc": _("Optional HTMX configuration for AJAX navigation.")}
    )


@dataclass
class StepperItemConfig:
    """
    Configuration for a step in the stepper component.

    Attributes:
        title: Title of the step.
        description: Additional description of the step below the title.
        url: URL called when the user clicks on the title of the step.
        success: Displays a checkmark instead of the step number.
        failed: Displays an X instead of the step number.
        current: Highlights the title in color and makes the text pulse.

    """

    __example__ = """
        StepperItemConfig(title="Address", description="Enter shipping address", success=True)
        """

    title: str = field(metadata={"doc": _("Title of the step.")})
    description: str = field(default="", metadata={"doc": _("Additional description of the step below the title.")})
    url: str = field(default="", metadata={"doc": _("URL called when the user clicks on the title of the step.")})
    success: bool = field(default=False, metadata={"doc": _("Displays a checkmark instead of the step number.")})
    failed: bool = field(default=False, metadata={"doc": _("Displays an X instead of the step number.")})
    current: bool = field(default=False, metadata={"doc": _("Highlights the title in color and makes the text pulse.")})


@dataclass
class StepperConfig:
    """
    Configuration for the stepper component.

    Renders a graphical representation of process steps.

    Attributes:
        items: List of step configurations.

    """

    __example__ = """
        StepperConfig(
            items=[
                StepperItemConfig(title="Address", description="Enter shipping address", success=True),
                StepperItemConfig(title="Payment", description="Select payment method", current=True),
                StepperItemConfig(title="Review", description="Review and confirm"),
            ],
        )
        """

    items: list[StepperItemConfig] = field(default_factory=list, metadata={"doc": _("List of step configurations.")})


@dataclass
class MinimalStepperConfig:
    """
    Configuration for the minimal_stepper component.

    Renders a compact progress indicator.

    Attributes:
        items: List of states for the process steps. Possible values: 'success', 'failed', 'active' and '' for inactive.
        step_count: Number of process steps. (Only if 'items' is not set!)
        current_step: Current step of the process. (Only if 'items' is not set!)
        current_step_status: Status of the current step. (Only if 'items' is not set!)
        icon_size: Size of the icons in the progress bar.

    """

    __example__ = """
        MinimalStepperConfig(step_count=5, current_step=3)
        """

    items: list[Literal["success", "failed", "active", ""]] = field(
        default_factory=list,
        metadata={
            "doc": _(
                "List of states for the process steps. Possible values: 'success', 'failed', 'active' and '' for inactive."
            )
        },
    )
    step_count: int = field(default=0, metadata={"doc": _("Number of process steps. (Only if 'items' is not set!)")})
    current_step: int = field(
        default=0, metadata={"doc": _("Current step of the process. (Only if 'items' is not set!)")}
    )
    current_step_status: Literal["active", "success", "failed"] = field(
        default="active", metadata={"doc": _("Status of the current step. (Only if 'items' is not set!)")}
    )
    icon_size: Literal["xs", "s", "m", "l", "xl"] = field(
        default="xs", metadata={"doc": _("Size of the icons in the progress bar.")}
    )


@dataclass
class BulletPointItemConfig:
    """
    Configuration for an item in the bullet_point_list component.

    Attributes:
        title: Title of the item.
        description: Additional description of the item below the title.
        request_url: The URL to be called when clicking on the respective item.
        completed: Displays a checkmark instead of a bullet point.
        current: Highlights the title by color.

    """

    __example__ = """
        BulletPointItemConfig(title="Setup", description="Initial configuration", completed=True)
        """

    title: str = field(metadata={"doc": _("Title of the item.")})
    description: str = field(default="", metadata={"doc": _("Additional description of the item below the title.")})
    request_url: str = field(
        default="", metadata={"doc": _("The URL to be called when clicking on the respective item.")}
    )
    completed: bool = field(default=False, metadata={"doc": _("Displays a checkmark instead of a bullet point.")})
    current: bool = field(default=False, metadata={"doc": _("Highlights the title by color.")})


@dataclass
class BulletPointListConfig:
    """
    Configuration for the bullet_point_list component.

    Renders a graphical representation of a bullet point list.

    Attributes:
        items: List of bullet point items.
        htmx: Optional HTMX configuration for AJAX navigation.

    """

    __example__ = """
        BulletPointListConfig(
            items=[
                BulletPointItemConfig(title="Setup", description="Initial configuration", completed=True),
                BulletPointItemConfig(title="Configure", description="Add settings", current=True),
                BulletPointItemConfig(title="Deploy", description="Push to production"),
            ],
        )
        """

    items: list[BulletPointItemConfig] = field(default_factory=list, metadata={"doc": _("List of bullet point items.")})
    htmx: HtmxConfig | None = field(
        default=None, metadata={"doc": _("Optional HTMX configuration for AJAX navigation.")}
    )


@dataclass
class AccordionItemConfig:
    """
    Configuration for an accordion section.

    Attributes:
        title: Section title.
        content: Section content.
        open: Whether section is initially open.

    """

    __example__ = """
        AccordionItemConfig(title="What is Django?", content="Django is...")
        """

    title: str = field(metadata={"doc": _("Section title.")})
    content: str = field(metadata={"doc": _("Section content.")})
    open: bool = field(default=False, metadata={"doc": _("Whether section is initially open.")})


@dataclass
class AccordionConfig:
    """
    Configuration for the accordion component.

    Renders expandable/collapsible sections.

    Attributes:
        tag_id: Unique tag ID for identifying the element in JavaScript.
        items: List of individual sections.
        exclusive: If **True** only one section can be open at a time.

    """

    __example__ = """
        AccordionConfig(
            tag_id="faq-accordion",
            items=[
                AccordionItemConfig(title="What is Django?", content="Django is..."),
                AccordionItemConfig(title="What is HTMX?", content="HTMX is..."),
            ],
            exclusive=True,
        )
        """

    tag_id: str = field(
        default="accordion", metadata={"doc": _("Unique tag ID for identifying the element in JavaScript.")}
    )
    items: list[AccordionItemConfig] = field(default_factory=list, metadata={"doc": _("List of individual sections.")})
    exclusive: bool = field(default=True, metadata={"doc": _("If **True** only one section can be open at a time.")})


@dataclass
class TabConfig:
    """
    Configuration for a single tab.

    Attributes:
        tag_id: Unique tag ID for identifying the element in JavaScript.
        title: Label of the tab button.
        url: The URL to be called when the tab is clicked.
        active: Whether this tab is initially active.

    """

    __example__ = """
        TabConfig(tag_id="general", title="General", url=reverse("conf_general"), active=True)
        """

    tag_id: str = field(metadata={"doc": _("Unique tag ID for identifying the element in JavaScript.")})
    title: str = field(metadata={"doc": _("Label of the tab button.")})
    url: str = field(default="", metadata={"doc": _("The URL to be called when the tab is clicked.")})
    active: bool = field(default=False, metadata={"doc": _("Whether this tab is initially active.")})


@dataclass
class TabsConfig:
    """
    Configuration for the tabs component.

    Renders a tabbed interface with HTMX content loading.

    Attributes:
        tag_id: Unique tag ID for identifying the element in JavaScript.
        tabs: List of tab buttons.
        label: Non-visible additional title that is to be read aloud by screen readers.

    """

    __example__ = """
        TabsConfig(
            tag_id="settings-tabs",
            label="Settings",
            tabs=[
                TabConfig(tag_id="general", title="General", url=reverse("conf_general"), active=True),
                TabConfig(tag_id="security", title="Security", url=reverse("conf_security")),
                TabConfig(tag_id="notifications", title="Notifications", url=reverse("conf_notifications")),
            ],
        )
        """

    tag_id: str = field(metadata={"doc": _("Unique tag ID for identifying the element in JavaScript.")})
    tabs: list[TabConfig] = field(metadata={"doc": _("List of tab buttons.")})
    label: str = field(
        default="", metadata={"doc": _("Non-visible additional title that is to be read aloud by screen readers.")}
    )

    def __post_init__(self) -> None:
        """Set the first tab as active if no tab is currently active."""
        if any(tab.active for tab in self.tabs):
            return

        self.tabs[0].active = True
