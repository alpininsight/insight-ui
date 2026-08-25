"""Demo rendering context for UI components."""

from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils.lorem_ipsum import paragraphs
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.brand import get_brand_logo_config, get_footer_description_defaults, get_navbar_brand_defaults
from insight_ui.component_details.component_context import get_demo_context, register_demo_context
from insight_ui.component_details.components import Component
from insight_ui.configs import (
    AccordionConfig,
    AccordionItemConfig,
    AppCardConfig,
    BadgeConfig,
    BrandMarkConfig,
    BreadcrumbItemConfig,
    BulletPointItemConfig,
    ButtonConfig,
    CardCarouselConfig,
    CardConfig,
    ChartConfig,
    ChartDatasetConfig,
    CheckboxConfig,
    CheckboxGroupConfig,
    CheckboxItemConfig,
    CornerRibbonConfig,
    DataAttrConfig,
    DropdownConfig,
    DropdownItemConfig,
    FilterConfig,
    FlipCardConfig,
    FooterConfig,
    FooterContactConfig,
    FormConfig,
    FormFieldConfig,
    GenericFilterConfig,
    GeoMapConfig,
    HeroConfig,
    HtmxConfig,
    IconConfig,
    ImageCarouselConfig,
    ImageCarouselItemConfig,
    ImageConfig,
    InfiniteScrollConfig,
    LegalNoticeConfig,
    LoginScreenConfig,
    LogoConfig,
    MinimalStepperConfig,
    ModalConfig,
    MultiselectConfig,
    NavbarConfig,
    NavbarLinkConfig,
    PaginationConfig,
    PaginationIppConfig,
    QueryBuilderFieldConfig,
    RadioBlockConfig,
    RadioGroupConfig,
    RadioItemConfig,
    SelectConfig,
    SidebarCategoryConfig,
    SidebarDataConfig,
    SidebarItemConfig,
    SliderConfig,
    StatusScreenConfig,
    StepperItemConfig,
    TabConfig,
    TableConfig,
    TabsConfig,
    ThreeDCarouselConfig,
    ToggleConfig,
    ToggleViewConfig,
    UserMenuConfig,
    UserMenuLinkConfig,
)
from insight_ui.demo_utils import generate_payload, map_payload_to_cards
from insight_ui.utils.pagination import get_page

# Some example filters for the filter example
model_type_options = {
    "placeholder": _("-- Select model --"),
    "language": _("Language Model"),
    "vision": _("Vision Model"),
    "multimodal": _("Multimodal Model"),
    "audio": _("Audio / Speech Processing"),
    "recommendation": _("Recommendation System"),
    "generative": _("Generative Model"),
}
runtime_options = {
    "placeholder": _("-- Select runtime --"),
    "cloud": _("Cloud (API-based)"),
    "edge": _("Edge / On-Device"),
    "local": _("Local (Self-hosted)"),
    "hybrid": _("Hybrid (Cloud + Local)"),
    "serverless": _("Serverless Deployment"),
}
license_options = {
    "placeholder": _("-- Select license --"),
    "free": _("Free / Open Source"),
    "freemium": _("Freemium"),
    "subscription": _("Subscription"),
    "pay_per_use": _("Pay per Use"),
    "enterprise": _("Enterprise License"),
}
DEMO_CARD_IMAGE_PATH = "insight_ui/favicon/android-chrome-512x512.png"

# Some example data for the query builder filter
DEMO_FIELDS = [
    QueryBuilderFieldConfig(
        "title",
        _("Title"),
        "text",
        {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "contains": _("contains (case sensitive)"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
    ),
    QueryBuilderFieldConfig(
        "description",
        _("Description"),
        "text",
        {"icontains": _("contains"), "contains": _("contains (case sensitive)")},
    ),
    QueryBuilderFieldConfig(
        "deadline",
        _("Deadline"),
        "date",
        {"date": _("is exact"), "date__gte": _("is not before"), "date__lte": _("is not after")},
    ),
    QueryBuilderFieldConfig(
        "client__name",
        _("Client"),
        "text",
        {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
    ),
]


def get_component_demo_context(component: Component) -> dict:
    """Serve component demo context."""
    context_func = get_demo_context(component)

    if not context_func:
        context_func = get_empty_context

    return context_func()


def get_login_screen_context() -> dict:
    """Serve context data for the login screen."""
    return (
        config.get_config()
        | get_footer_context()
        | {
            "content_fill": True,
            "login_config": LoginScreenConfig(
                logo=get_brand_logo_config(height="8rem"),
                show_theme_toggle=True,
                forgot_password_url="#",  # noqa: S106  # nosec B106 - placeholder URL
                alt_login_url="#",
                alt_login_title=_("Login with OIDC"),
                sign_up_url="#",
            ),
        }
    )


# =============================================================
#
#   Layout Tags
#
# =============================================================


@register_demo_context(Component.HERO)
def get_hero_context() -> dict:
    """Serve demo context for the hero component."""
    return {
        "hero_config": HeroConfig(
            "Insight UI",
            _("Front-end Design Made Easy"),
            _("A modern UI library for Django applications to get started quickly."),
            ButtonConfig(label=_("Get Started"), request_url="#", type="primary", icon=IconConfig("rocket-launch")),
            ButtonConfig(label=_("Learn more"), request_url="#", type="secondary"),
            badge_config=BadgeConfig("Django UI Library", IconConfig("sparkles")),
        )
    }


@register_demo_context(Component.STATUS_SCREEN)
def get_status_screen_context() -> dict:
    """Serve demo context for the status screen component."""
    return {
        "status_screen_success": StatusScreenConfig(
            _("You're signed in"),
            [
                _("The authentication flow completed successfully."),
                _("You can now continue to the application."),
            ],
            "success",
            BrandMarkConfig(
                "Insight",
                "UI",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="3rem"
                ),
            ),
            _("Session ready"),
            _("This screen is generic and can be reused for auth, deployment, or workflow states."),
            ButtonConfig(label=_("Continue"), request_url="#", type="primary"),
            ButtonConfig(label=_("Back to start"), request_url="#", type="secondary"),
        ),
        "status_screen_error": StatusScreenConfig(
            _("Sign-in failed"),
            _("The SSO process could not be completed."),
            "error",
            BrandMarkConfig(
                "Insight",
                "UI",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="3rem"
                ),
            ),
            _("What happened?"),
            _("Please try again or contact support if the issue persists."),
            ButtonConfig(label=_("Try again"), request_url="#", type="primary"),
            ButtonConfig(label=_("Contact support"), request_url="#", type="secondary"),
        ),
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register_demo_context(Component.NAVBAR)
def get_navbar_context() -> dict:
    """Serve data for navbar detailpage."""
    return {
        "demo_nav_config": NavbarConfig(
            brand=get_navbar_brand_defaults(),
            links=[
                NavbarLinkConfig(_("Startpage"), "/", IconConfig("home", "s")),
                NavbarLinkConfig(
                    _("About"),
                    modal=ModalConfig(
                        "about-modal",
                        _("About Insight-UI"),
                        _("A modern UI library for Django applications to get started quickly."),
                    ),
                ),
                NavbarLinkConfig(_("Test"), "/", need_auth=True),
                NavbarLinkConfig(_("Test2"), "/", need_auth=True, staff_only=True),
            ],
            searchbar_request_url="/",
            enable_doc_search=True,
            usermenu=UserMenuConfig(
                links=[
                    UserMenuLinkConfig(
                        text=_("Settings"),
                        request_url=reverse("index_view"),
                        icon="cog-8-tooth",
                    ),
                    UserMenuLinkConfig(
                        text=_("Administration"),
                        request_url=reverse("admin:index"),
                        staff_only=True,
                        icon="home",
                    ),
                    UserMenuLinkConfig(
                        text=_("Translation"),
                        request_url=reverse("index_view"),
                        staff_only=True,
                        icon="globe-alt",
                    ),
                ],
            ),
            show_language_selector=True,
            show_theme_toggle=True,
        ),
    }


@register_demo_context(Component.SIDEBAR)
def get_drawer_context() -> dict:
    """Serve data for sidebar detailpage."""
    return {
        "demo_sidebar_data": SidebarDataConfig(
            _("Settings"),
            IconConfig("wrench-screwdriver", "s"),
            [
                SidebarCategoryConfig(
                    _("Work"),
                    IconConfig("building-office-2", "s"),
                    [
                        SidebarItemConfig(_("Notifications"), reverse("index_view"), IconConfig("bell", "s")),
                        SidebarItemConfig(
                            _("Messages"), reverse("index_view"), IconConfig("chat-bubble-left-right", "s")
                        ),
                        SidebarItemConfig(
                            _("Tasks"), reverse("index_view"), IconConfig("clipboard-document-check", "s")
                        ),
                    ],
                ),
                SidebarCategoryConfig(
                    _("Management"),
                    IconConfig("cog-8-tooth", "s"),
                    [
                        SidebarItemConfig(_("Calendar"), reverse("index_view"), IconConfig("calendar", "s")),
                        SidebarItemConfig(_("Profile"), reverse("index_view"), IconConfig("user", "s")),
                    ],
                ),
            ],
        )
    }


@register_demo_context(Component.FOOTER)
def get_footer_context() -> dict:
    """Server data for footer detailpage."""
    return {
        "footer_config": FooterConfig(
            get_footer_description_defaults(),
            [
                NavbarLinkConfig(_("Startpage"), "/", IconConfig("home", "xs")),
                NavbarLinkConfig(_("Storybook"), "/"),
                NavbarLinkConfig(_("Documentation"), "/"),
            ],
            FooterContactConfig(
                "support@alpininsight.com", "https://alpininsight.com/imprint/", "https://alpininsight.com/privacy/"
            ),
            get_legal_notice_context()["legal_notice_config"],
            "v1.0.0",
        )
    }


@register_demo_context(Component.BREADCRUMBS)
def get_breadcrumb_context() -> dict:
    """Serve data for breadcrumbs detailpage."""
    return {
        "breadcrumb_items": [
            BreadcrumbItemConfig(_("Startpage"), "/", IconConfig("home", "s")),
            BreadcrumbItemConfig(_("Components"), "/"),
            BreadcrumbItemConfig(_("Breadcrumbs")),
        ],
        "single_breadcrumb_item": [BreadcrumbItemConfig(_("Startpage"), icon=IconConfig("home", "s"))],
    }


@register_demo_context(Component.STEPPER)
def get_stepper_context() -> dict:
    """Serve data for step bar detailpage."""
    return {
        "stepper_items": [
            StepperItemConfig(_("Contact Details"), _("Information about the person and address."), success=True),
            StepperItemConfig(_("Payment Method"), _("Select the payment method."), current=True),
            StepperItemConfig(_("Review"), _("Review the data and pay.")),
        ],
        "stepper_items_failed": [
            StepperItemConfig(_("Contact Details"), _("Information about the person and address."), success=True),
            StepperItemConfig(_("Payment Method"), _("Select the payment method."), success=True),
            StepperItemConfig(_("Review"), _("Review the data and pay."), failed=True),
        ],
    }


@register_demo_context(Component.MINIMAL_STEPPER)
def get_minimal_stepper_context() -> dict:
    """Serve data for minimal step bar detailpage."""
    return {
        "min_stepper": MinimalStepperConfig(step_count=5, current_step=3),
        "min_stepper_with_list": MinimalStepperConfig(["success", "success", "failed", "active", ""]),
    }


@register_demo_context(Component.BULLET_POINT_LIST)
def get_bullet_point_list_context() -> dict:
    """Server data for bullet point list detailpage."""
    return {
        "bullet_points_items": [
            BulletPointItemConfig(_("Contact Details"), _("Information about the person and address."), completed=True),
            BulletPointItemConfig(_("Payment Method"), _("Select the payment method."), current=True),
            BulletPointItemConfig(_("Review"), _("Review the data and pay.")),
        ]
    }


@register_demo_context(Component.ACCORDION)
def get_accordion_context() -> dict:
    """Serve data for accordion detailpage."""
    return {
        "accordion_config": AccordionConfig(
            "faq",
            [
                AccordionItemConfig(_("What is Django?"), _("Django is a web framework for Python.")),
                AccordionItemConfig(_("What is Tailwind?"), _("Tailwind is a CSS utility framework")),
                AccordionItemConfig(_("What is ARIA?"), _("ARIA is short for Accessible Rich Internet Applications.")),
            ],
            False,
        )
    }


@register_demo_context(Component.TABS)
def get_tabs_context() -> dict:
    """Serve data for tabs detailpage."""
    return {
        "tabs_config": TabsConfig(
            "settings-tabs",
            [
                TabConfig("general", _("General"), reverse("tabs_view", kwargs={"tab_id": "first"})),
                TabConfig("security", _("Security"), reverse("tabs_view", kwargs={"tab_id": "second"})),
                TabConfig("notification", _("Notification"), reverse("tabs_view", kwargs={"tab_id": "third"})),
            ],
            _("Settings"),
        )
    }


# =============================================================
#
#   Input Tags
#
# =============================================================


@register_demo_context(Component.CHECKBOX)
def get_checkbox_context() -> dict:
    """Serve data for checkbox detailpage."""
    return {
        "checkbox_config": CheckboxConfig(
            "accept-terms", "accept_terms", _("I accept the terms and conditions"), required=True, value="accepted"
        )
    }


@register_demo_context(Component.CHECKBOX_GROUP)
def get_checkbox_group_context() -> dict:
    """Serve data for checkbox group detailpage."""
    return {
        "checkbox_group_config": CheckboxGroupConfig(
            "language",
            _("Choose languages: (max. 3)"),
            [
                CheckboxItemConfig("english", _("English"), "english"),
                CheckboxItemConfig("german", _("German"), "german"),
                CheckboxItemConfig("french", _("French"), "french"),
                CheckboxItemConfig("spanish", _("Spanish"), "spanish"),
                CheckboxItemConfig("italian", _("Italian (currently not available)"), "italian", True),
            ],
            True,
            1,
            3,
        )
    }


@register_demo_context(Component.DROPDOWN)
def get_dropdown_context() -> dict:
    """Serve data for dropdown detailpage."""
    return {
        "user_dropdown_config": DropdownConfig(
            "user",
            _("User"),
            items=[
                DropdownItemConfig(_("Profile"), "/", IconConfig("user", "s")),
                DropdownItemConfig(_("Settings"), "/", IconConfig("cog-8-tooth", "s")),
                DropdownItemConfig(_("Logout"), "/", IconConfig("arrow-left-on-rectangle", "s")),
            ],
        ),
        "settings_dropdown_config": DropdownConfig(
            "settings",
            _("Settings"),
            False,
            [
                DropdownItemConfig(_("Personal Information"), "/", IconConfig("user", "s")),
                DropdownItemConfig(_("Appearance"), "/", IconConfig("cog-8-tooth", "s")),
            ],
        ),
    }


@register_demo_context(Component.RADIO_GROUP)
def get_radio_group_context() -> dict:
    """Serve data for radio group detailpage."""
    return get_radio_block_context() | {
        "model_radio_config": RadioGroupConfig(
            "model",
            _("Select AI Model:"),
            [
                RadioItemConfig("model1", "BERT", _("BERT")),
                RadioItemConfig("model2", "PaLM 2", _("PaLM 2")),
                RadioItemConfig("model3", "LLaMA 2", _("LLaMA 2 (currently not available)"), disabled=True),
            ],
        )
    }


@register_demo_context(Component.RADIO_BLOCK)
def get_radio_block_context() -> dict:
    """Serve data for radio block detailpage."""
    return {
        "view_radio_config": RadioBlockConfig(
            "view",
            _("Select view mode:"),
            items=[
                RadioItemConfig("card-view", "card", icon=IconConfig("squares-2x2")),
                RadioItemConfig("table", "table", icon=IconConfig("list-bullet")),
                RadioItemConfig("card-carousel", "carousel", icon=IconConfig("square-3-stack-3d"), disabled=True),
            ],
        ),
        "size_radio_config": RadioBlockConfig(
            "size",
            _("Select size:"),
            items=[
                RadioItemConfig("small-size", "small", "s"),
                RadioItemConfig("medium-size", "medium", "m"),
                RadioItemConfig("large-size", "large", "l", disabled=True),
            ],
            as_row=True,
        ),
    }


@register_demo_context(Component.RANGE_SLIDER)
def get_range_slider_context() -> dict:
    """Serve data for range-slider detailpage."""
    return {
        "slider_skip_config": SliderConfig(
            "range-slider-skip",
            "range_slider_skip",
            _("Legend Mode: Skip"),
            value=6,
            minimum=1,
            maximum=12,
            items=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            legend_mode="skip",
        ),
        "slider_rotate_config": SliderConfig(
            "range-slider-rotate",
            "range_slider_rotate",
            _("Legend Mode: Rotate"),
            value=6,
            minimum=1,
            maximum=12,
            items=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            legend_mode="rotate",
        ),
        "slider_dual_config": SliderConfig(
            "range-slider-dual",
            "range_slider_dual",
            _("Dual Range Slider"),
            minimum=0,
            maximum=1000,
            value_min=200,
            value_max=800,
            items=["0€", "250€", "500€", "750€", "1000€"],
            dual=True,
        ),
    }


@register_demo_context(Component.TOGGLE)
def get_toggle_button_context() -> dict:
    """Serve data for toggle-button detailpage."""
    return {
        "switch_config": ToggleConfig("toggle-switch", "toggle-switch", _("Click me!"), switch=True),
        "toggle_config": ToggleConfig("toggle-button", "toggle-button", _("Click me!")),
    }


@register_demo_context(Component.SELECT)
def get_select_context() -> dict:
    """Serve data for select detailpage."""
    return {
        "select_config": SelectConfig(
            "capital", "capital", _("Capitals:"), options=[_("Berlin"), _("Rome"), _("London")]
        )
    }


@register_demo_context(Component.MULTISELECT)
def get_multiselect_context() -> dict:
    """Serve data for multiselect detailpage."""
    return {
        "multiselect_config": MultiselectConfig(
            "capital",
            "capital",
            _("Capitals:"),
            maximum=3,
            show_buttons=True,
            options=[_("Berlin"), _("Rome"), _("London"), _("Brussels"), _("Paris"), _("Warsaw")],
            selected_options=[_("Rome"), _("Berlin")],
        )
    }


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register_demo_context(Component.MODAL)
def get_modal_context() -> dict:
    """Serve data for the modal detailpage."""
    return {
        "confirm_modal_config": ModalConfig(
            "action-demo-modal",
            _("Demo modal"),
            _("This is an example of a standard modal."),
            [
                ButtonConfig(label=_("Yes, confirm"), type="primary", on_click="alert('Confirmed!')"),
                ButtonConfig(
                    label=_("Abort"), type="secondary", data_attrs=[DataAttrConfig("insight-dismiss", "modal")]
                ),
            ],
        )
    }


# =============================================================
#
#   Util Tags
#
# =============================================================


@register_demo_context(Component.LEGAL_NOTICE)
def get_legal_notice_context() -> dict:
    """Serve data for legal notice detailpage."""
    return {
        "legal_notice_config": LegalNoticeConfig(
            2026, "Alpin Insight Solutions GmbH & Co. KG", "Open Source", "AGPL-3.0", reverse_lazy("license_view")
        )
    }


@register_demo_context(Component.DIFFERENTIATOR)
def get_differentiator_context() -> dict:
    """Serve data for differentiator detailpage."""
    return {"textA": _("The cat is sleeping on the red sofa."), "textB": _("This is a completely different sentence!")}


@register_demo_context(Component.LOGO)
def get_logo_context() -> dict:
    """Serve data for logo detailpage."""
    return {
        "logo_svg_config": LogoConfig(
            "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="3rem"
        ),
        "logo_image_config": LogoConfig(
            "insight_ui/favicon/android-chrome-192x192.png", alt="Insight UI app icon", height="3rem"
        ),
        "logo_icon_config": LogoConfig(icon=IconConfig("sparkles", "xl"), alt="Decorative product icon"),
    }


@register_demo_context(Component.BRAND_MARK)
def get_brand_mark_context() -> dict:
    """Serve data for brand mark detailpage."""
    return {
        "brand_mark_default": BrandMarkConfig(
            "Alpin Insight",
            "Solutions",
            LogoConfig("insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="3rem"),
        ),
        "brand_mark_end": BrandMarkConfig(
            "Alpin Insight",
            "Platform",
            LogoConfig("insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="3rem"),
            "end",
        ),
    }


@register_demo_context(Component.CORNER_RIBBON)
def get_corner_ribbon_context() -> dict:
    """Serve data for corner ribbon detailpage."""
    return {
        "ribbon_top_right": CornerRibbonConfig(_("New Feature"), "top-right", "primary"),
        "ribbon_top_left": CornerRibbonConfig(_("Verified"), "top-left", "success"),
        "ribbon_bottom_right": CornerRibbonConfig(_("Beta"), "bottom-right", "warning"),
        "ribbon_bottom_left": CornerRibbonConfig(_("Limited"), "bottom-left", "danger"),
        "ribbon_info": CornerRibbonConfig(_("Info"), "top-right", "info"),
    }


@register_demo_context(Component.GEO_MAP)
def get_geo_map_context() -> dict:
    """Serve data for geo-map detailpage."""
    return {
        "geo_map_config": GeoMapConfig(
            [52.5200, 13.4050],
            8,
            36,
            [
                {
                    "name": "population",
                    "type": "circle",
                    "min": 300000,
                    "max": 3800000,
                    "data": [
                        {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
                        {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
                        {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
                        {"title": "Köln", "value": 1086000, "lat": 50.9375, "lon": 6.9603},
                        {"title": "Frankfurt am Main", "value": 763000, "lat": 50.1109, "lon": 8.6821},
                        {"title": "Stuttgart", "value": 635000, "lat": 48.7758, "lon": 9.1829},
                        {"title": "Düsseldorf", "value": 620000, "lat": 51.2277, "lon": 6.7735},
                        {"title": "Leipzig", "value": 612000, "lat": 51.3397, "lon": 12.3731},
                        {"title": "Dortmund", "value": 588000, "lat": 51.5136, "lon": 7.4653},
                        {"title": "Essen", "value": 582000, "lat": 51.4556, "lon": 7.0116},
                        {"title": "Bremen", "value": 569000, "lat": 53.0793, "lon": 8.8017},
                        {"title": "Dresden", "value": 558000, "lat": 51.0504, "lon": 13.7373},
                        {"title": "Hannover", "value": 540000, "lat": 52.3759, "lon": 9.7320},
                        {"title": "Nürnberg", "value": 523000, "lat": 49.4521, "lon": 11.0767},
                        {"title": "Duisburg", "value": 499000, "lat": 51.4344, "lon": 6.7623},
                        {"title": "Bochum", "value": 363000, "lat": 51.4818, "lon": 7.2162},
                        {"title": "Wuppertal", "value": 361000, "lat": 51.2562, "lon": 7.1508},
                        {"title": "Bielefeld", "value": 341000, "lat": 52.0302, "lon": 8.5325},
                        {"title": "Bonn", "value": 330000, "lat": 50.7374, "lon": 7.0982},
                        {"title": "Münster", "value": 323000, "lat": 51.9607, "lon": 7.6261},
                    ],
                },
                {
                    "name": "hanseatic_cities",
                    "type": "marker",
                    "data": [
                        {
                            "title": "Lübeck",
                            "lat": 53.8655,
                            "lon": 10.6866,
                            "description": "Hauptstadt der Hanse („Königin der Hanse“); Sitz der Hansetage und Zentrum des Ostseehandels.",
                        },
                        {
                            "title": "Hamburg",
                            "lat": 53.5511,
                            "lon": 9.9937,
                            "description": "Wichtiger Nordseehafen; Umschlagplatz für den England- und Nordseehandel.",
                        },
                        {
                            "title": "Bremen",
                            "lat": 53.0793,
                            "lon": 8.8017,
                            "description": "Bedeutend im England- und Skandinavienhandel; Nordseezugang der Hanse.",
                        },
                        {
                            "title": "Köln",
                            "lat": 50.9375,
                            "lon": 6.9603,
                            "description": "Größte Stadt der Hanse; zentraler Binnenhandelsknoten am Rhein.",
                        },
                        {
                            "title": "Danzig (Gdańsk)",
                            "lat": 54.3520,
                            "lon": 18.6466,
                            "description": "Wichtigster Hafen im Ostseeraum; Export von Getreide, Holz und Bernstein.",
                        },
                        {
                            "title": "Riga",
                            "lat": 56.9496,
                            "lon": 24.1052,
                            "description": "Zentrum des Hansehandels im Baltikum; Umschlagplatz für Waren aus Russland und Skandinavien.",
                        },
                        {
                            "title": "Reval (Tallinn)",
                            "lat": 59.4370,
                            "lon": 24.7536,
                            "description": "Wichtige Zwischenstation für Russland- und Skandinavienhandel.",
                        },
                        {
                            "title": "Visby",
                            "lat": 57.6409,
                            "lon": 18.2960,
                            "description": "Frühes Hansezentrum auf Gotland; Knotenpunkt des Ostseehandels.",
                        },
                        {
                            "title": "Bergen",
                            "lat": 60.3913,
                            "lon": 5.3221,
                            "description": "Kontorstadt der Hanse in Norwegen; Handel mit Stockfisch und Pelzen.",
                        },
                        {
                            "title": "Brügge",
                            "lat": 51.2093,
                            "lon": 3.2247,
                            "description": "Zentrale für Tuchhandel in Flandern; wichtiges westliches Handelszentrum.",
                        },
                        {
                            "title": "London (Stalhof)",
                            "lat": 51.5074,
                            "lon": -0.1278,
                            "description": "Hanse-Kontor für den Englandhandel; Sitz des „Stalhofs“ im Mittelalter.",
                        },
                        {
                            "title": "Nowgorod",
                            "lat": 58.5215,
                            "lon": 31.2755,
                            "description": "Östlichstes Hansekontor; Handel mit Fellen, Wachs und Honig im Russlandgeschäft.",
                        },
                    ],
                },
            ],
        )
    }


@register_demo_context(Component.CHART)
def get_charts_context() -> dict:
    """Serve data for charts detailpage."""
    return {
        "chart_config": ChartConfig(
            "chart",
            ChartDatasetConfig(
                _("Chart Example"),
                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
                [
                    [100, 302, 301, 334, 390, 330, 320],
                    [320, 132, 101, 134, 90, 230, 210],
                    [220, 182, 191, 234, 290, 330, 310],
                    [150, 212, 201, 154, 190, 330, 410],
                    [820, 832, 901, 934, 1290, 1330, 1320],
                ],
            ),
        )
    }


# =============================================================
#
#   List Tags
#
# =============================================================


@register_demo_context(Component.INFINITE_SCROLL)
def get_infinite_scroll_context() -> dict:
    """Serve data for infinite scroll detailpage."""
    return {
        "infinite_scroll_config": InfiniteScrollConfig(
            "news-feed",
            reverse("more_items"),
            [
                {"title": _("Element %(i)s") % {"i": i}, "content": _("Content for element %(i)s") % {"i": i}}
                for i in range(1, 11)
            ],
        )
    }


@register_demo_context(Component.PAGINATION)
def get_pagination_context() -> dict:
    """Serve data for pagination detailpage."""
    page_obj, surrounding_pages = get_page(generate_payload(500))
    ipp_config = PaginationIppConfig("ipp", _("Items per page"), options=[10, 20, 30])

    return {"pagination_config": PaginationConfig(reverse("pagination"), page_obj, surrounding_pages, ipp_config)}


@register_demo_context(Component.TABLE)
def get_table_context() -> dict:
    """Serve data for table detailpage."""
    return {
        "table_config": TableConfig(
            [_("Name"), _("E-Mail"), _("Status"), _("Actions")],
            [
                ["Max Mustermann", "max@example.com", _("Active"), '<button class="btn btn-primary">Edit</button>'],
                ["Anna Schmidt", "anna@example.com", _("Inactive"), '<button class="btn btn-primary">Edit</button>'],
                ["Tom Weber", "tom@example.com", _("Active"), '<button class="btn btn-primary">Edit</button>'],
            ],
            _("Example of a table component."),
        )
    }


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register_demo_context(Component.GENERIC_FILTER)
def get_generic_filter_context() -> dict:
    """Serve data for generic filter detailpage."""
    return {
        "generic_filter_config": GenericFilterConfig(
            [
                FilterConfig(
                    "model_type_filter",
                    _("AI model type"),
                    model_type_options,
                    _("To filter by the type of AI-Model."),
                    IconConfig("rocket-launch", "s"),
                ),
                FilterConfig(
                    "runtime_filter",
                    _("Runtime"),
                    runtime_options,
                    _("To filter by the runtime."),
                    IconConfig("clock", "s"),
                ),
                FilterConfig("license_filter", _("License"), license_options, icon=IconConfig("document-text", "s")),
            ],
            "/",
        )
    }


@register_demo_context(Component.QUERY_BUILDER)
def get_query_builder_context() -> dict:
    """Serve data for the query-builder detailpage."""
    return {"model_fields": DEMO_FIELDS}


# =============================================================
#
#   Card Tags
#
# =============================================================


@register_demo_context(Component.CARD)
def get_card_context() -> dict:
    """Serve data for card detailpage."""
    return {
        "cards_config": [
            CardConfig(_("Example Card"), _("Subtitle"), _("This is the card content.")),
            CardConfig(
                _("Card with actions"),
                content=_("This card has some action buttons."),
                actions=[
                    ButtonConfig(label=_("Learn more"), request_url="#", type="secondary"),
                    ButtonConfig(label=_("Share"), request_url="#", type="primary"),
                ],
            ),
        ]
    }


@register_demo_context(Component.APP_CARD)
def get_app_card_context() -> dict:
    """Serve data for app card detailpage."""
    return {
        "app_card_config": AppCardConfig(
            _("App Card"),
            _("A card with its content arranged horizontally."),
            image=ImageConfig(static(DEMO_CARD_IMAGE_PATH), _("Card-Image")),
            tags=[
                BadgeConfig(label=_("Insight UI"), type="primary", size="xs"),
                BadgeConfig(label=_("Layout"), type="secondary", size="xs"),
                BadgeConfig(label=_("Card"), type="info", size="xs"),
            ],
            actions=[
                ButtonConfig(label=_("Learn more"), request_url="#", type="secondary"),
                ButtonConfig(label=_("Share"), request_url="#", type="primary"),
            ],
        )
    }


@register_demo_context(Component.FLIP_CARD)
def get_flip_card_context() -> dict:
    """Serve data for flip card detailpage."""
    return {
        "flip_card_config": FlipCardConfig(
            title=_("Flip Card"),
            content=_("A card with additional details on the back. Click the arrow to flip."),
            back_title=_("More Details"),
            back_content=_("Here you can add extended information without taking more space on the page."),
            back_actions=[
                ButtonConfig(label=_("Contact"), request_url="#", type="primary", outline=True),
            ],
            image=ImageConfig(static(DEMO_CARD_IMAGE_PATH), _("Card-Image")),
            tags=[
                BadgeConfig(label=_("Insight UI"), type="primary", size="xs"),
                BadgeConfig(label=_("Layout"), type="secondary", size="xs"),
                BadgeConfig(label=_("Card"), type="info", size="xs"),
            ],
            actions=[
                ButtonConfig(label=_("Learn more"), request_url="#", type="secondary"),
                ButtonConfig(label=_("Share"), request_url="#", type="primary"),
            ],
        )
    }


@register_demo_context(Component.CARD_CAROUSEL)
def get_card_carousel_context() -> dict:
    """Serve data for card carousel detailpage."""
    return {
        "carousel_config": CardCarouselConfig(
            map_payload_to_cards(generate_payload()), show_index=True, items_per_slide=2
        )
    }


@register_demo_context(Component.IMAGE_CAROUSEL)
def get_image_carousel_context() -> dict:
    """Serve data for image carousel detailpage."""
    seeds = ["neuschwanstein", "berlin-night", "hamburg-harbour"]
    lorem_blocks = paragraphs(len(seeds), common=False)

    return {
        "image_carousel_config": ImageCarouselConfig(
            [
                ImageCarouselItemConfig(
                    f"https://picsum.photos/seed/{seed}/1200/675",
                    _("Placeholder image %(index)s") % {"index": index + 1},
                    lorem_blocks[index],
                )
                for index, seed in enumerate(seeds)
            ],
            show_index=True,
        )
    }


@register_demo_context(Component.THREE_D_CAROUSEL)
def get_3d_carousel_context() -> dict:
    """Serve data for 3D carousel detailpage."""
    return {
        "3D_carousel_config": ThreeDCarouselConfig("showcase", map_payload_to_cards(generate_payload()), 300, -15, True)
    }


@register_demo_context(Component.TOGGLE_VIEW)
def get_toggle_view_context() -> dict:
    """Serve data for toggle-view detailpage."""
    return {
        "toggle_view_config": ToggleViewConfig(
            "products-view",
            cards=map_payload_to_cards(generate_payload()),
            view_radio_config=RadioBlockConfig(
                "products-view-toggle",
                items=[
                    RadioItemConfig("card-view", "card", icon=IconConfig("squares-2x2")),
                    RadioItemConfig("table-view", "table", icon=IconConfig("list-bullet")),
                    RadioItemConfig("carousel-view", "carousel", icon=IconConfig("square-3-stack-3d")),
                ],
                request_url=reverse("toggle_view"),
            ),
        )
    }


# =============================================================
#
#   Form Tags
#
# =============================================================


@register_demo_context(Component.FORM)
def get_form_context() -> dict:
    """Serve data for form detailpage."""
    return {
        "form_config": FormConfig(
            "register-form",
            _("Registration"),
            _("Sign up to get access to our whole product portfolio."),
            [
                FormFieldConfig(
                    "select",
                    "title",
                    "title",
                    _("Title"),
                    _("Your title"),
                    options=[_("No title"), "Prof.", "Dr.", _("King")],
                ),
                FormFieldConfig(
                    "text", "firstname", "firstname", _("First name"), _("Type in your first name"), required=True
                ),
                FormFieldConfig(
                    "text", "lastname", "lastname", _("Last name"), _("Type in your last name"), required=True
                ),
                FormFieldConfig(
                    "email", "email", "email", _("E-mail"), _("Type in your.email@example.com"), required=True
                ),
                FormFieldConfig(
                    "password", "password", "password", _("Password"), _("Type in your password"), required=True
                ),
                FormFieldConfig(
                    "textarea", "message", "message", _("Message"), _("Do you want to tell us something?..."), rows=5
                ),
            ],
            True,
            htmx_config=HtmxConfig(target="#htmx-form"),
        )
    }


def get_empty_context() -> dict:
    """Serve an empty dictionary."""
    return {}
