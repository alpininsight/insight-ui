"""Configuration classes for navigation components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import HtmxConfig, IconConfig
from insight_ui.configs.input import DropdownConfig
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import CopyrightNoticeConfig, LogoConfig


@dataclass
class NavbarBrandConfig:
    """
    Configuration for the navbar brand section.

    Attributes:
        title: Brand title text.
        request_url: Brand link URL.
        logo: Logo configuration.
        gap: CSS gap between logo and title.

    """

    title: str = ""
    request_url: str = ""
    logo: LogoConfig | None = None
    gap: str = "0.5rem"


@dataclass
class NavbarLinkConfig:
    """
    Configuration for a navbar navigation link.

    Attributes:
        text: Link text.
        url: Direct URL, if not opening a modal or dropdown menu.
        icon: Optional icon configuration.
        need_auth: Only show to authenticated users.
        staff_only: Only show to staff users.
        open_modal: Configuration of a modal dialog.
        open_dropdown: Configuration of a dropdown menu.

    """

    text: str
    url: str = ""
    icon: IconConfig | None = None
    need_auth: bool = False
    staff_only: bool = False
    modal: ModalConfig | None = None
    dropdown: DropdownConfig | None = None


@dataclass
class NavbarConfig:
    """
    Configuration for the navbar component.

    Renders a full navigation bar with brand, links, and optional features.

    Attributes:
        brand: Brand section configuration.
        links: List of navigation links.
        searchbar_request_url: Url for search functionality.
        show_usermenu: Show user menu dropdown.
        show_language_selector: Show language selection dropdown.
        show_theme_toggle: Show dark/light theme toggle.

    Example:
        >>> navbar = NavbarConfig(
        ...     brand=NavbarBrandConfig(
        ...         title="My App",
        ...         request_url=reverse("index"),
        ...         logo=LogoConfig(url="img/logo.svg", height="2rem"),
        ...     ),
        ...     links=[
        ...         NavbarLinkConfig(text="Home", request_url=reverse("index")),
        ...         NavbarLinkConfig(text="About", request_url=reverse("about")),
        ...         NavbarLinkConfig(text="Admin", request_url=reverse("admin:index"), staff_only=True),
        ...     ],
        ...     show_usermenu=True,
        ...     show_theme_toggle=True,
        ... )

    """

    brand: NavbarBrandConfig | None = None
    links: list[NavbarLinkConfig] = field(default_factory=list)
    searchbar_request_url: str = ""
    show_usermenu: bool = False
    show_language_selector: bool = False
    show_theme_toggle: bool = False


@dataclass
class SidebarItemConfig:
    """
    Configuration for a sidebar navigation item.

    Attributes:
        text: Item text.
        request_url: Target URL.
        icon: Optional icon configuration.
        htmx: HTMX configuration for AJAX page changes.

    """

    text: str
    request_url: str = ""
    icon: IconConfig | None = None
    htmx: HtmxConfig | None = None


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

    caption: str
    icon: IconConfig | None = None
    items: list[SidebarItemConfig] = field(default_factory=list)
    collapsed: bool = False


@dataclass
class SidebarDataConfig:
    """
    Configuration for sidebar content.

    Attributes:
        title: Sidebar title.
        icon: Optional title icon.
        categories: List of navigation categories.

    """

    title: str = ""
    icon: IconConfig | None = None
    categories: list[SidebarCategoryConfig] = field(default_factory=list)


@dataclass
class SidebarConfig:
    """
    Configuration for the sidebar component.

    Renders a side navigation panel.

    Attributes:
        sidebar_data: Sidebar content configuration.
        side: Which side to display ('left' or 'right').
        static: If True, sidebar is always visible.
        auto_close: If True, sidebar closes when mouse leaves.
        mobile_hidden: If True, hide on mobile viewports.

    Example:
        >>> sidebar = SidebarConfig(
        ...     sidebar_data=SidebarDataConfig(
        ...         title="Settings",
        ...         categories=[
        ...             SidebarCategoryConfig(
        ...                 caption="Account",
        ...                 items=[
        ...                     SidebarItemConfig(text="Profile", request_url=reverse("profile")),
        ...                     SidebarItemConfig(text="Security", request_url=reverse("security")),
        ...                 ],
        ...             ),
        ...         ],
        ...     ),
        ...     side="left",
        ...     static=True,
        ... )

    """

    sidebar_data: SidebarDataConfig | None = None
    side: Literal["left", "right"] = "right"
    static: bool = True
    auto_close: bool = False
    mobile_hidden: bool = False


@dataclass
class FooterDescriptionConfig:
    """
    Configuration for the footer description section.

    Attributes:
        title: Section title.
        text: Description text.
        logo: Optional image/logo configuration.

    """

    title: str = ""
    text: str = ""
    logo: LogoConfig | None = None


@dataclass
class FooterContactConfig:
    """
    Configuration for footer contact information.

    Attributes:
        mail_url: Email address or mailto URL.
        imprint: Imprint page URL.
        privacy: Privacy policy URL.

    """

    mail_url: str = ""
    imprint: str = ""
    privacy: str = ""


@dataclass
class FooterConfig:
    """
    Configuration for the footer component.

    Renders a complete page footer.

    Attributes:
        description: Description section configuration.
        links: List of footer links.
        contact: Contact information.
        copyright: Copyright notice configuration.
        version: Application version string.

    Example:
        >>> footer = FooterConfig(
        ...     description=FooterDescriptionConfig(
        ...         title="My App",
        ...         text="A modern web application.",
        ...     ),
        ...     links=[
        ...         NavbarLinkConfig(text="Home", request_url=reverse("index")),
        ...         NavbarLinkConfig(text="Docs", request_url="https://docs.example.com"),
        ...     ],
        ...     contact=FooterContactConfig(
        ...         mail_url="support@example.com",
        ...         imprint="/imprint/",
        ...         privacy="/privacy/",
        ...     ),
        ...     copyright=CopyrightNoticeConfig(
        ...         year=2026,
        ...         holder="My Company",
        ...     ),
        ...     version="v1.0.0",
        ... )

    """

    description: FooterDescriptionConfig | None = None
    links: list[NavbarLinkConfig] = field(default_factory=list)
    contact: FooterContactConfig | None = None
    copyright: CopyrightNoticeConfig | None = None
    version: str = ""


@dataclass
class BreadcrumbItemConfig:
    """
    Configuration for a breadcrumb navigation item.

    Attributes:
        text: Breadcrumb text.
        request_url: Target URL.
        icon: Optional icon (typically for home item).

    """

    text: str
    request_url: str = ""
    icon: IconConfig | None = None


@dataclass
class StepBarItemConfig:
    """
    Configuration for a step in the step_bar component.

    Attributes:
        title: Step title.
        description: Step description.
        url: URL called when the user clicks on the title of the step.
        success: Whether step is completed successfully.
        failed: Whether step failed.
        current: Whether this is the current step.

    Example:
        >>> steps = [
        ...     StepBarItemConfig(title="Address", description="Enter shipping address", success=True),
        ...     StepBarItemConfig(title="Payment", description="Select payment method", current=True),
        ...     StepBarItemConfig(title="Review", description="Review and confirm"),
        ... ]

    """

    title: str
    description: str = ""
    url: str = ""
    success: bool = False
    failed: bool = False
    current: bool = False


@dataclass
class MinimalStepBarConfig:
    """
    Configuration for the minimal_step_bar component.

    Renders a compact progress indicator.

    Attributes:
        items: List of step statuses ('success', 'failed', 'active', '').
        step_count: Total number of steps (used if items is empty).
        current_step: Current step index (0-based, used if items is empty).
        current_step_status: Status for current step ('active', 'success', 'failed').
        icon_size: Icon size for step indicators.

    Example using items directly:
        >>> progress = MinimalStepBarConfig(
        ...     items=["success", "success", "active", "", ""],
        ...     icon_size="xs",
        ... )

    Example using step_count and current_step:
        >>> progress = MinimalStepBarConfig(
        ...     step_count=5,
        ...     current_step=2,
        ...     current_step_status="active",
        ...     icon_size="xs",
        ... )

    """

    items: list[Literal["success", "failed", "active", ""]] = field(default_factory=list)
    step_count: int = 0
    current_step: int = 0
    current_step_status: Literal["active", "success", "failed"] = "active"
    icon_size: Literal["xs", "s", "m", "l", "xl"] = "xs"


@dataclass
class BulletPointItemConfig:
    """
    Configuration for an item in the bullet_point_list component.

    Attributes:
        title: Item title.
        description: Item description.
        request_url: Optional link URL.
        completed: Whether item is marked as completed.
        current: Whether this is the current item.

    Example:
        >>> checklist = [
        ...     BulletPointItemConfig(title="Setup", description="Initial configuration", completed=True),
        ...     BulletPointItemConfig(title="Configure", description="Add settings", current=True),
        ...     BulletPointItemConfig(title="Deploy", description="Push to production"),
        ... ]

    """

    title: str
    description: str = ""
    request_url: str = ""
    completed: bool = False
    current: bool = False


@dataclass
class AccordionItemConfig:
    """
    Configuration for an accordion section.

    Attributes:
        title: Section header text.
        content: Section content (can include HTML).
        open: Whether section is initially open.

    """

    title: str
    content: str
    open: bool = False


@dataclass
class AccordionConfig:
    """
    Configuration for the accordion component.

    Renders expandable/collapsible sections.

    Attributes:
        tag_id: Unique ID for the accordion.
        items: List of accordion sections.
        exclusive: If True, only one section can be open at a time.

    Example:
        >>> faq = AccordionConfig(
        ...     tag_id="faq-accordion",
        ...     items=[
        ...         AccordionItemConfig(title="What is Django?", content="Django is..."),
        ...         AccordionItemConfig(title="What is HTMX?", content="HTMX is..."),
        ...     ],
        ...     exclusive=True,
        ... )

    """

    tag_id: str = "accordion"
    items: list[AccordionItemConfig] = field(default_factory=list)
    exclusive: bool = True


@dataclass
class TabConfig:
    """
    Configuration for a single tab.

    Attributes:
        tag_id: Unique ID for this tab.
        title: Tab button text.
        url: URL for tab content (loaded via HTMX).
        active: Whether this tab is initially active.

    """

    tag_id: str
    title: str
    url: str = ""
    active: bool = False


@dataclass
class TabsConfig:
    """
    Configuration for the tabs component.

    Renders a tabbed interface with HTMX content loading.

    Attributes:
        tag_id: Unique ID for the tabs container.
        label: Accessible label for the tab list.
        tabs: List of tab configurations.

    Example:
        >>> tabs = TabsConfig(
        ...     tag_id="settings-tabs",
        ...     label="Settings",
        ...     tabs=[
        ...         TabConfig(tag_id="general", title="General", request_url=reverse("conf_general"), active=True),
        ...         TabConfig(tag_id="security", title="Security", request_url=reverse("conf_security")),
        ...         TabConfig(tag_id="notifications", title="Notifications", request_url=reverse("conf_notifications")),
        ...     ],
        ... )

    """

    tag_id: str
    label: str = ""
    tabs: list[TabConfig] = field(default_factory=list)
