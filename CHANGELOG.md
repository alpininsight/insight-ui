# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Bug Fixes

- **license:** Use contact@alpininsight.ai for commercial licensing enquiries
- **a11y:** Hide the idle HTMX loading indicator from the accessibility tree
- **ci:** Preserve public contributor title validation
- **release:** Correct package defaults and retire duplicate publisher
- **deps:** Align tzdata lock with generated requirements
- Remove unintended spaces if 'brand_mark' does not contain a logo or symbol
- Remove unintended color transition from the 'sidebar'
- Correct compponent parameter validation issues
- Correct the if statements so that 'navbar' and 'footer' are not displayed when the corresponding configuration is None
- Correct disabled button colors
- Solve 'tooltip' overlaps trigger and is initial visible when opening modal or drawer
- Make 'list' use VALID_SPACING_WITH_NONE for the gap parameter
- Use correct user object in the navbar
- **ci:** Enforce public workflow boundary for every trigger
- **sidebar:** Use one mobile drawer lifecycle controller
- **navbar:** Preserve language form return URL
- **sidebar:** Use one mobile drawer lifecycle controller
- **devtools:** Isolate and validate contributor tooling
- **devtools:** Reject unexported config collisions
- **devtools:** Preserve scaffold safety and validation gates
- **build:** Pin Tailwind compiler and verify version consistency
- **packaging:** Use absolute public documentation links
- **readme:** Label hero bubble Django-Insight-UI
- **readme:** Refresh Django Insight UI hero

### CI/CD

- Adopt the standard Alpine Insight workflow callers
- **cdn:** Add a CDN asset verification gate

### Documentation

- **readme:** Name the product Django-Insight-UI
- Update developer documentation
- Update readme
- **contributing:** Clarify documentation-ready component handoff
- **readme:** Add Django Packages badge

### Features

- Set 'navbar_fixed' to False per default
- Validate icon names and show suggestions for typos
- Check for typos in the parameters of the 'button' component
- Add validation for the layout tag parameters and add None as possible option for 'gap' and 'padding'
- Add optional 'navbar' and 'footer' the the login template
- Convert 'modal' component to a layout tag
- Add parameters for the text colors to the 'brand_mark' component
- Add new component 'list' as layout tag
- Add config classes for the 'list' and 'modal' layout tag
- Simplify the use of the horizontal list
- Add sizes for icon only buttons and show the label automatically as tooltip
- Remove hard reference of the dialog element for the 'modal' component
- Add a gap between logo and titel on the login screen
- Use the outline button variant for the 'user_dropdown'
- Add 'id' as parameter to the layout tags
- Add flag token parameter handling for the layout tags
- Remove CopyrightNoticeConfig alias
- Drastically simplify the preview app
- Improve demo container controls
- **devtools:** Integrate contributor playground from PR #651

### Miscellaneous

- **sync:** Align release preparation with main
- Set executable bit for the manage.py
- Fix distribution check
- Slightly adjust linting settings
- Consolidate the 'Hatchling' configuration in one place

### Testing

- Fix JavaScript tests
- Fix license hashes
- **cdn:** Guard the verification manifest against drift
- **tailwind:** Align wrapper reproducibility pin

## [1.14.0] - 2026-09-09

### Bug Fixes

- Correct template path for playground view
- Use 'INSIGHT_UI' context settings for 'navbar_fixed' instead of a hidden variable
- Correct layout of the 'badge' and 'button' demo on mobile devices
- Remove gap below sidebar in the sidebar demo
- Add 'side' to the oob swap sidebar on docs detailpages
- 'parameter table' id is undefined error when navigating via browser history
- **navbar:** Render user menu icon names
- Declare AGPL-3.0 in pyproject classifiers
- **container:** Pin Uvicorn wheel dependency
- **a11y:** Separate semantic action and foreground tokens
- **a11y:** Repair catalog component semantics
- **a11y:** Use the primary foreground token for the page header title
- **docs:** Replace conformance claims with designed-to-conform wording
- **css:** Cover dynamic package color variants
- **navigation:** Distinguish fragment targets
- **ui:** Keep branded headings and wordmarks readable
- **ui:** Package responsive brand mark styles
- **ci:** Stop manual CDN deploys from rolling back the latest alias
- **scaffold:** Reject conflicting imports and render composition labels
- **license:** Keep LICENSE verbatim and pin the licence text hashes

### CI/CD

- **package:** Exclude legacy application sources
- Thin caller for central package SBOM workflow
- Send package SBOM to insight-ui-docs
- **contributors:** Isolate public package checks

### Documentation

- **cdn:** Add required CDN asset manifest and delivery/entitlement contract
- **cdn:** Scope manifest as verify-subset and reconcile insight-ui vs insight-brand
- **cdn:** Keep verification contract deployment-neutral
- Fix outdated test paths in testing.md
- **license:** Clarify AGPL or Commercial spurwahl in stub
- **contributors:** Explain component workflow with a diagram
- Correct contact email for commercial licensing inquiries
- **contributors:** Restore package guides and verify README examples
- **readme:** Point to the prepared Enterprise documentation next to the scope limit

### Features

- **button:** Support theme-specific secondary foregrounds
- Make 'grid' centrable
- Reverse the change to make the 'button', 'radio_block' and 'toggle' container agnostic
- Rename 'url' to 'request_url' for 'CarouselItemConfig', 'TabsConfig', StepperItemConfig' and the 'NavbarLinkConfig'
- Improve general validation and default values of component configs
- Hide the entire section in the footer if the corresponding config is not specified
- Add CSRF token globally to hx headers
- Add 'GET' support to 'form' component
- Add color token support to 'icon' component
- Show qoutes for an empty value in the types registry
- Use a wider variety of values for the different badge sizes
- Add documentation and explanations to the design tokens in the input.css
- Add htmx support to navbar and footer links
- Move docs links from the navbar to the sidebar
- Make placeholder and button labels configurable for 'search_bar' and 'form'
- Use the 'SearchBarConfig' for the search bar in the navbar
- Update translations
- Update search indices
- Change favicon and logo
- Add id's to 'background_image' and 'header' blocks
- Add HTMX support to 'dropdown' component
- New Logo and Favicon
- Rename 'HTMXMethod' to 'HTTPMethod' and use it for 'form' component method parameter
- **corner-ribbon:** Support accessible link actions
- Preparation for publishing on PyPI
- Text tokens
- **contributors:** Scaffold atomic component compositions
- **contributors:** Add loopback-only component preview

### Miscellaneous

- **package:** Separate documentation test suite
- **license:** Add SPDX headers, REUSE metadata and third-party notices

### Refactoring

- **package:** Move documentation ownership to insight-ui-docs

### Reverted

- Chore(package): seperate documentation test suit

### Styling

- **corner-ribbon:** Format linked ribbon template

### Testing

- Add test accordingly to the new validation improvements
- Restructure tests

## [1.13.2] - 2026-08-31

### Bug Fixes

- **config:** Retain copyright notice compatibility alias
- **package:** Ship documentation app in wheel

## [1.13.1] - 2026-08-30

### Miscellaneous

- **static:** Generate minified assets only in CI

### Testing

- **sidebar:** Await drawer opening animation

## [1.13.0] - 2026-08-30

### Bug Fixes

- **charts:** Correct accessible data table values
- **docs:** Wrap demo controls on narrow screens
- Correct polygon of 'minimal_stepper' for rtl mode
- Correct animation and chevron direction of the sidebar component in RTL mode
- Set 'navbar_fixed' for the toc sidebar to prevent the label from disappearing
- Remove sidebar shift in mobile browsers
- Remove the need to specify the 'request_url' twice for the 'search_bar' component
- **htmx:** Serialize config values as JSON
- Make radio item gray if disabled and set default cursor
- Use 'parameter_table' on icon detailpage instead of include the template directly
- Correct check method for the 'double request_url' warning
- **brand-mark:** Render the wordmark accent in Signal Orange
- Use correct url for login screen
- Use white text instead of base text color for the 'radio_block' component
- Restore old active state design for sidebar navigation links
- **brand-mark:** Stop rendering template comment
- Remove tooltip and popup instance on delete
- Actually disable 'multiselect' and 'select' when disabled is 'True'
- Remove mistyped 's' from 'range_slider' dual mode
- Rotate the chevron icon of the 'breadcrumb' component by 180° in RTL mode
- **cdn:** Support historical candidate asset builds
- Update paths in commands to match the new documentation structure
- **docs:** Wire localized search index

### CI/CD

- **pypi:** Publish via Trusted Publishing instead of an API token
- Rerun standard checks on PR title edits
- **cdn:** Publish candidate assets from image source

### Documentation

- Align self-documentation app references

### Features

- Update 'sidebar' parameter description and example code
- Sync navbar and sidebar response behavior
- Show a warning when the developer sets both, the component 'request_url' and HTMXConfig 'request_url'
- Determine current page via aria attributes and add highlighting for navbar dropdown menus
- Remove 'Home' from navbar
- Use a more suitable icon for the language toggle
- Add 'UserMenuConfig', 'LoginScreenConfig' and add 'register_url' to 'navbar' component
- Add 'content_fill' option for the base template
- Add version information to 'copyright_notice' and rename component to 'legal_notice'
- Add 'disabled' parameter to the 'button' component and remove 'disabled' from ButtonType
- Make disabled inputs more decent and add 'disabled_reason' parameter to input components
- Add dict support for 'options' of the 'FormFieldConfig' and move list to dict converting logic to corresponding configs
- Add new component descriptions and lists with core features to each component
- Update translations
- Add config based usage examples to 'breadcrumbs', 'stepper' and 'bullet_point_list' components
- Add more different examples to the 'button' and 'badge' usage examples
- Add captions to the 'badge' demo and make the captions in the 'button' demo smaller
- Add support for container queries to 'grid' component and add more demo examples
- Add 'weight' and 'style' parameter to the 'divider' component and a dedicated color token
- Add optional label to the 'divider' component
- Add 'h-fit' to 'button', 'badge', 'radio_block' and 'toggle_button' component
- Add responsive behavior to the 'article' component
- Change app name to 'Django Insight UI' in the navbar
- Use a more distinguishable background color for the 'modal' component in dark mode
- Make the 'sort_utility_classes' script ignore comments
- Create app 'documentation' and move all related files to this new app
- Update translations
- Update translations

### Refactoring

- Return drawer context directly whitout creating temp variable

### Reverted

- **pypi:** Restore token-based publish until prerequisites exist

### Testing

- Add smoke tests for the docs pages
- Change language to english for the component parameter context tests
- Update navbar and login screen tests
- Update tests
- **brand-mark:** Assert rendered wordmark contract

## [1.12.0] - 2026-08-20

### Bug Fixes

- Add missing data-attribute support to the template file of the 'button' component
- Update usage documentation parameter of the 'footer', 'sidebar' and 'app_card' component
- Remove the reference to the deprecated 'type' parameter of the 'logo' component from the docuemntation
- Minimal_stepper retains its size even after all steps have been completed
- Move special base template parameters from get_navbar_context to get_base_context
- Fix typo in usage example of the command for generating minified assets
- **component-scaffold:** Align generated component contracts
- **component-scaffold:** Use semantic token classes
- **test:** Document radius token checks
- **i18n:** Compile translations in container build
- **theme:** Preserve generated css newline
- Change 'BrandLockupConfig' to 'BrandMarkConfig' in 'status_screen' component
- **brand:** Align defaults with brand mark
- **i18n:** Translate homepage copy
- Set default for LogoConfig in BrandMarkConfig to None and BrandMarkConfig in StatusScreenConfig too
- **static:** Update generated tailwind asset
- **static:** Refresh generated tailwind asset
- Issues related to latest translation changes
- Change old icon names in the 'alert' component and in the component demo container
- Adjust 'type' to 'info_type' in the 'infobox' template
- Using proper text color class for the 'brand_mark' component
- **cdn:** Publish insight ui browser assets
- **cdn:** Trigger release asset publishing
- **theme:** Use semantic tokens for search UI
- Whitespace handling in the new sort_utility_classes script
- Set executable bit on sort_utility_classes.py
- Rename 'surface_link' to 'surface' in the index page template
- Correct a measuring bug in cleanIndentation method of the 'code_block' component
- Remove inconsistencies and minor issues on the documentation pages
- Correct various issues in the JavaScript components
- **static:** Preserve generated stylesheet newline
- **static:** Build complete CDN assets
- **deps:** Sync generated requirements with uv lock
- **container:** Refresh Debian security packages
- Use correct template for htmx swap of component detailpages
- Add alternating row colors for parameter tables again

### Build System

- **static:** Refresh generated tailwind asset

### CI/CD

- Migrate digest-pin to least-privilege app token
- **user-dropdown:** Refresh required checks
- **static:** Guard Tailwind theme asset sync
- **cdn:** Publish release assets from release workflow
- **cdn:** Pin CDN version in GitOps updates

### Documentation

- **ci:** Refresh digest-pin token comment to app-token setup
- **theme:** Document semantic motion roles
- **brand:** Align settings example with brand mark
- **deployment:** Use canonical insight ui develop host
- Add missing docstrings to JavaScript code
- Reorganize and cleanup developer documentation
- Remove 'assets' directory from developer documentation
- Update 'Documentation' part of the README
- Update readme
- Remove internal operations details

### Features

- Add 'button' component
- Add 'badge' component
- Set configs for 'button' and 'badge' in components.py
- Add 'progress_bar' component
- Add label, process text and tooltip to 'progress_bar'
- Add request functionality to 'progress_bar' for polling or via sse
- Add custom 'data-attribute' support to 'button' component
- Add mouse-follow and text update support to 'tooltip' component
- Use 'button' and 'tooltip' component in 'progress_bar' component
- Add badge color variants and badge size variants
- Add round button design
- Replace 'ActionConfig' with 'ButtonConfig'
- Remove obsolete htmx-extension.js and use corresponding htmx-attributes instead
- Replace raw href tag with 'button' component for 'pagination' and 'user_dropdown'
- **navbar:** Tokenize bar surface/border/shadow + item radius for theming
- Add layout components 'page', 'vbox', 'hbox', 'grid', 'spacer' and 'divider'
- Add index page
- Add neutral type for the outline and subtle button variants
- Increase h tag font size
- Add v_align parameter to 'page' component and rename align and justify to v_align and h_align
- Improve documentation and examples of the 'page', 'vbox', 'hbox', 'spacer' and 'divider'
- **theme:** Introduce semantic surface tokens
- **navbar:** Introduce semantic icon button token
- **sidebar:** Introduce semantic icon button token
- **user-dropdown:** Introduce semantic panel tokens
- **progress-bar:** Introduce semantic track tokens
- **chat:** Introduce semantic response bubble tokens
- **table:** Introduce semantic surface tokens
- **forms:** Introduce semantic status tokens
- **theme:** Introduce semantic shadow roles
- **theme:** Introduce semantic radius roles
- **status-screen:** Align component with semantic tokens
- **brand:** Add settings based brand defaults
- Remove obsolete title config member
- Replace underscores with hyphens in icon names
- Add 'compile_icons' command to generate icons.html from svg files
- Update indentation calculation and docstrings of the 'compile_icons' command
- Add all outline heroicons to icon library and add 'compile_icons' command description to icons detailpage
- Update used icons by using official heroicons name and no alias
- Href in the 'button' component is no longer set when disabled
- Update icons of the 'status_screen' component to use new names
- Make 'brand_mark' using 'logo' component instead of hardcoded icons
- Add translations for the icons detailpage and fix fuzzy translations
- **deployment:** Set insight-ui.com production canonical
- Add 'Size' type and a validation function instead of repeatedly using hardcoded Literals
- Add types for the 'corner_ribbon', 'button' and 'badge' color values
- Add 'StepStatus' type for 'minimal_stepper'
- Add 'AlertType' type for 'alert', 'status_screen' and 'infobox' component
- Add 'HtmlButtonType' type for the 'button' component
- Add 'CornerPosition' type for the 'corner_ribbon' component
- Add 'HorizontaleSide' and 'InlinePosition' type
- Add 'FilterFildType' for the 'query_builder' component
- Add 'HtmlInputType' and 'FormFieldType' for generel input fields and for explicit form fields
- Add 'HtmxSwapMethod' and 'HtmxMethod' type for the HTMXConfig
- Add 'GeoMapMarkerType' type for the 'geo_map' component
- Add 'SliderLegendMode' type for the 'range_slider' component
- Add 'ToggleViewType' type for the 'toggle_view' component
- Add missing translations
- Remove 'title' and 'logo' from NavbarBrandConfig and use BrandMarkConfig instead
- **theme:** Bridge surface role tokens to the brand colour contract
- **cards:** Tokenize card + image_carousel surfaces/borders to semantic roles
- Add new colors
- Add soft colors
- Add background and border colors
- Replace Tailwind tokens for rounded corners with custom tokens controlled via input.css
- Use custom spacing tokens for layout tags
- Replace Tailwind tokens for shadows with custom tokens controlled via input.css
- Replace all hardcoded colors, shadows and roundings with design tokens
- Use proper names for background colors
- Add search functionality for the documentation via the search bar in the navbar
- Add custom types detailpage and add popups to the parameter tables for the custom types
- Add new installation page layout with further information
- Add surface and link_surface layout tags and use layout tags for the installation page layout
- Refactor 'tabs' and 'collapsible' components to layout tags
- Use 'tabs' and 'collapsible' components on installation page
- Use new 'surface' and 'link_surface' layout tag on the index page
- Use design tokens for colors in the 'code_block' component
- Reduce padding for the sidebars and the navbar
- Refactor sidebar to layout tag
- Add 'prefix' parameter to 'page_header' for adding a prefix to the title
- Improve 'base template' page with example mockup and updated texts
- Add 'section' layout tag and merge 'link_surface' and 'surface' to 'surface'
- Modify the 'check_design_token' script to search only in class strings for tokens
- Place 'prefix' in the 'page_header' component after the title and rename the parameter to 'chapter'
- Remove top margin from 'infobox' component
- Use 'section' layout tag in the base_template and the icons template
- Remove default padding from h tags and add utility classes for some colors and combined surface classes
- Update heading and pb 0 from h tags on installation page
- Improve 'customization' page with graphical elements and more information
- Add 'none' as valid value for 'divider' spacing
- Add 'id' parameter to 'surface' layout tag
- Use more subtle color for odd rows in 'table' components
- Improve component detailpage layout
- Wrap storybook pages in a vbox
- Add 'ignore' flag to toc generator to ignore single headings
- Integrate new websocket demo into the main django application
- Add missing aria hidden arguments to 'form' and 'infinite_scroll' components
- Add escape event handler and keyboard navigation to 'dropdown', 'modal', 'sidebar' and 'popup' components
- Add 'role' attributes to multiple components
- Use 'fieldset' and 'legend' for 'radio_group', 'radio_block' and 'checkbox_group' components
- Add 'role' and 'roledescription' to carosuel components
- Add appropriate aria attributes to 'popup' and 'tooltip' components
- Improve a11y for multiple components
- Add keybord navigation to carousels and remove default value from 'alt' text parameter for the image carousel
- Add announcement for reaching the min or max value of the 'checkbox_group' component
- Improve a11y of the 'query_builder' component using groups and unique id's
- Add keybord navigation and aria labels to the 'geo_map' component
- Add screenreader table, aria labels and decal pattern to chart components
- Add flip button to  and use  component for the tags
- Use semantic correct  tag for  component
- Meta information
- Configure webmanifest and add maskable icons
- Responsiveness
- Config class reference page

### Miscellaneous

- **navbar:** Apply formatter output
- **ignore:** Exclude playwright cli artifacts
- Add pre-commit hook for checking used design tokens in templates
- Mark check_design_tokens script as executable
- Update dependencies
- Update node dependencies
- Update pre commit hooks and fix linting
- Format websocket demo readme
- Fix uv.lock
- **static:** Regenerate assets after rebase
- Add --no-minify to rebuild stylesheet command

### Refactoring

- Remove redundant loading of script files in base.html and components.html
- Reduce hardcoded index page tokens
- **theme:** Semantic range control tokens
- **brand:** Rename brand mark component
- Move type definitions to separate file
- Move html code for the search results to a separate template file
- Sort css classes in all templates
- Move 'layout' directory to components directory
- Change indentation mode from tabs to spaces for the 'tabs' and 'sidebar' script files
- Replace structlog with stdlib logging
- Remove old websocket demo subproject 'utils'

### Testing

- **forms:** Keep status include within line limit
- **theme:** Document shadow token checks
- **i18n:** Document container translation contract
- **i18n:** Avoid compiled catalog dependency
- Update JavaScript tests
- Add new tests for JavaScript components
- Move JavaScript tests to main tests directory
- Adjust tests for new accessibility
- Adjust tests and remove unnecessary css class checks

## [1.11.0] - 2026-06-18

### Bug Fixes

- Correct linting and remove print statements (T201) from ignored issues
- Correct size of the 'corner_ribbon' component for non default positions
- Remove 'user' and 'show_login' parameter for the navbar component from templates
- **sidebar:** Keep primary docs navigation visible
- **brand-lockup:** Use public icons and document navbar mode
- **brand-lockup:** Preserve icon sizing and variant compatibility
- **brand-lockup:** Handle legacy positional size calls
- **dataclasses:** Port brand lockup after develop merge
- **static:** Refresh generated tailwind assets
- **card:** Keep actions inside long content cards
- **card:** Restore template and constrain actions
- **card:** Preserve image card sizing
- Repair dataclass component regressions
- Preserve nested config behavior
- Align radio block integration semantics
- Preserve pagination page configs
- **ci:** Run container publish on every branch push
- **ci:** Pin only published container digests

### CI/CD

- **cdn:** Upload static assets by branch alias
- Use central reusable workflows

### Documentation

- **cdn:** Document static asset delivery

### Features

- Introduce dataclasses instead of dictionaries for component configuration
- Add consistent config namespace to each component
- Add href links to component documentation of several components
- Add metadata with field documentation to component config dataclasses
- Standardize insight_tags and add config override support for kwargs
- Remove 'user' and 'show_login' parameter from navbar component
- Use 'IconConfig' for icon docu page icons
- Add config dataclass for several components
- Generate component parameter documentation from dataclass documentation
- Use component demo containers for storybook pages
- **component:** Add brand_lockup — final-symbol logo + two-tone wordmark
- **brand_lockup:** Add per-environment wing variant param
- Allow HTML code in card content
- **card:** Add formatted content demos
- Rename 'insight_websocket' component to 'websocket'
- Update component usage examples with new config dataclass examples
- Add 'create_component' command which generates boilerplate code for new components
- **navbar:** Support user avatar trigger
- Add links to the component demos that lead to the corresponding files in the Git repository
- Improvements

### Miscellaneous

- Correct linting
- Normalize changelog whitespace
- Add missing __init__ files for new 'create_component' command
- **ci:** Retrigger repository policy after workflow promotion

### Styling

- Format pagination dataclass test

### Testing

- Update tests to use dataclass based config system for the component tests
- Split component tests into seperate files
- Apply django-upgrade header style

## [1.10.3] - 2026-06-01

### Bug Fixes

- **navbar:** Sync user dropdown position to develop

## [1.10.2] - 2026-05-27

### Bug Fixes

- **alert:** Correct tage_id typo in alert template tag return dict
- DestroyAllIn() container-as-root bug and Floater selector mismatch
- Merge issues in the carousel components
- **js:** Wire lifecycle cleanup class lookup and carousel selector
- **security:** Update dependencies to resolve all 16 vulnerabilities
- **ci:** Probe django container readiness internally
- **ui:** Replace missing homepage static asset
- **ci:** Use PAT token for pre-commit autoupdate PRs
- **ci:** Enable multi-arch container build for arm64 support
- Misspelled component names
- Navbar and sidebar demo in the navigation storybook
- Page header for storybook and component details pages
- Add missing description texts for storybooks
- Add missing docs context for the 'radio_block' component
- Remove obsolete special handling of the 'radio_block' component
- JavaScript test and bump undici version to 7.24.0
- Broken component demos
- Add configurable data and static roots
- Annotate health check view
- Function naming radio_block
- Function declarations demo_context, checkbox_group
- Rome translation ID
- Add some missing translatable strings in the demo_context.py
- Get_radio_block_description_context() naming declaration
- Resolve merge conflict in django.po
- Radio_block_parameter_context() declaration
- Demo_context, replace f-string to make it translatable
- Make 'toggle' component accessible for keyboard navigation
- Visualize focus for 'radio_block' component
- Add loading indicator to partial responses
- Use blocktrans for multiline strings in some templates
- Integration test checks now for success status, not the potentially tranlated string.
- Add missing string markers, correct spelling
- String fixes
- Change login smoke test to check for NOT translated string rather in comments
- Minor spelling
- **ci:** Restore automatic release on develop→main merge
- **docs:** Resolve component-slug regressions (toggle_button, outline_button, button_sizes, effect_cards)
- **ci:** Update scheduled pre-commit workflow actions
- **deps:** Update vulnerable dependencies
- **docs:** Use manifest-safe card demo assets
- **docs:** Serve component source links locally
- **static:** Require explicit cdn opt-in
- **static:** Preserve selectors in minified css assets
- **cards:** Stabilize app card layout
- **navbar:** Keep user dropdown out of layout flow
- **navbar:** Position user dropdown below trigger

### CI/CD

- Automate release-please PR checks and merge
- **guard:** Preserve branch-policy check name
- **guard:** Preserve branch-policy check name
- **feature:** Mirror required legacy test checks
- Allow stacked branch pull requests
- Align blue/green container publish and promotion
- Use central reusable container workflow
- **container:** Enable manual django image builds

### Documentation

- Add component architecture requirements
- **guides:** Add component architecture epic backlog
- **backlog:** Update with Sprint 1 completion status
- Rewrote and translate contributing.md
- Translate developer documentation
- Add hint to run JavaScript tests to README.md
- Make component docu context strings translateable
- Document GitHub issue label taxonomy
- Remove README workflow badges
- Reflect Django support range in badge
- Add notification component mockups
- Move insight ui audit into repo
- Document design system contract
- Add component self-documentation checklist
- Document documentation architecture

### Features

- **js:** Add destroy() lifecycle methods to all components
- **security:** Replace inline onclick handlers with event delegation
- Sprint 3 standardization - 3D-Carousel and documentation
- **tests:** Add JavaScript test infrastructure with Vitest
- Improve JavaScript debug logging
- Connect JavaScript instances with corresponding html tags
- Add lifecycle support to code block component
- Add lifecycle support to collapsibles
- Add lifecycle support to theme toggles
- Add lifecycle support to demo containers
- Use instance and tag connection for proper cleanup
- **container:** Add django runtime image workflow
- Add component decorator and dispatcher for component context methods
- Fill a11y documentation context with current data
- Fill description documentation context with current data
- Fill usage documentation context with current data
- Update parameter documentation context structure
- Add missing git link for hero component documenation
- Add related topic entries for page_header, article and hero component
- Adjust new component documentation base template and add markdown as dependency
- Handle empty lists in the component details template
- Add Component Enum Class as component registry
- Add registration system for the component demo contexts
- Rename 'cog' icon to 'gear'
- Add new components automatically to sidebar navigation and corresponding storybook
- Add non partial version of the new storybook and component details pages
- Add share icon
- Add 'django-rosetta' as dev dependency
- Translate function docs of the insight_tags
- Add translatable strings to the index, base_template, customization, icons and installation templates
- Make the current step of the minimal_step_bar configurable
- Add an url parameter to the steps of the steps_bar and make them klickable
- Replace DE with EN strings
- Added EN translation fields
- In progress 22 % translation EN to DE
- Exchange DE to EN text strings
- Description_context.py with EN strings
- 50%  EN strings replaced
- Changes all translatable strings to EN in parameter_context.py
- EN-DE translations for parameter_context.py
- Context.py added new and replaced msgid to EN, added DE translations
- Views.py add and replace msgid to EN, add DE translations
- Demo_utils.py add EN to DE translations
- Replaced and added EN msgids for all .html templates
- EN to DE translations for all .html
- Sharpen fuzzy translations
- Add new setting 'use_tailwind_cli' and remove obsolete env-variables
- Add heading decoration component
- Remove detailpages
- Add logo component
- **stream:** Clarify HTMX websocket boundary
- **runtime:** Prepare blue-green demo deployment contract
- Add copyright notice component
- Improvements
- Standardize the JavaScript lookup attribute naming convention
- Enhancements
- **static:** Publish minified assets via cdn

### Miscellaneous

- **config:** Add CLAUDE.md to gitignore and dockerignore
- Add .playwright-mcp to gitignore
- Remove checklists from docs
- **ci:** Migrate from release-please to GitVersion
- Update requirements.txt
- Consistent Insight UI spelling
- Update package-lock.json
- Update uv.lock
- Update footer copyright notice
- **docs:** Remove legacy mkdocs layer
- **ci:** Refresh GitHub Actions for Node 24
- Release develop to main

### Refactoring

- Change toc generator indentation from two to four whitespaces
- Remove special parameter context handling from views.py
- Remove hardcoded list of components from smoke tests
- Rename 'table' and 'main' storybook
- Remove obsolete storybook template files
- Adopt logo component

### Reverted

- Get_component_demo_context() linter warning

### Testing

- Improve smoke tests for storybooks and fix loginscreen test
- Use Component Enum Class for smoke tests
- Js tests

## [1.10.0] - 2026-04-08

### Miscellaneous

- Release insight-ui — sync develop→main (5 months of work)

## [1.9.1] - 2026-02-24

### Bug Fixes

- Hide static docs sidebars on smaller viewports

### CI/CD

- Add changelog workflow from insight-ci template

## [1.9.0] - 2026-02-19

### Bug Fixes

- Carousel rtl issue
- Toggle_view demo issue
- Footer links always link to current page
- Usage of old variable name for the id in the alert, infinit scroll and card component
- That the dropdown menu briefly appears after page reload
- Chat field is not cleared after submit
- Align tests with pagination API rewrite
- **dev:** Resolve Server Error 500 after fresh clone
- Add min-w-0 to content area flex child to prevent overflow
- Prevent navbar link text from wrapping
- Shorten sidebar title and fix TOC sidebar padding
- Sidebar height and remove container style from component detail pages
- Step_bar component misspelling issue
- Minimal_step_bar demo

### CI/CD

- Add branch policy validation and complete PR title types

### Features

- Add submit Button to form by default and make reset button optional via bool parameter
- Display unachieved bullet points in gray, in the bullet point component
- Add installation page
- Add tailwind setup instructions to customization page
- Add icons page
- Add base_template page
- Align layout of the component detailpage, the icons, customization and installation page
- Add alternating row colors to the table component
- Improve sidebar demo content
- Use icon component for alert icons
- Use icon component for language toggle
- Add optional privacy link to footer component and improve footer documentation
- Turn JavaScript classes to modules and fix browser history related htmx request issue
- Change htmx-indicator display method from inline to flex
- Create ToC class and completely rewrite ToC script
- Add ToC to base_template, icons and installations page
- Make radio_block item id's more unique
- Add ipp select to pagination and decouple pagination from list
- Add new 'heading' block to base template
- Add minimal step bar compoenent
- Add HTMX support for breadcrumb component
- Add HTMX support for bulletpoint component
- Add HTMX support for dropdown component
- Add HTMX support for searchbar component
- Add HTMX support for generic_filter component
- Change from view_name to url for chat component request
- Add 'failed' status option to step bar component
- **toc:** Redesign TOC sidebar with circle button and in-flow layout
- Add new components, detail pages, and context helpers
- Add 'hero' component
- Add 'layout' storybook
- Add documentation of the 'minimal_step_bar' component
- Add new component detailpage base template
- Add 'link' icon

### Miscellaneous

- Pin and update all dependencies
- **docs:** Remove completed architecture guide documents
- **docs:** Remove obsolete index.md and fix README links

### Refactoring

- Move component detail context files to dedicated directory
- Remove component docs from the development documentation
- Flatten dev docu hierarchy
- Improve modal component code
- Change line indentation of the live_content component
- Centralize content area wrapper in base.html
- Update sidebar

### Testing

- Fix footer test
- Add smoke tests for missing components

## [1.8.0] - 2026-01-26

### Bug Fixes

- Add missing config parameter 'fixed' to navbar tag
- Wrong id on bullet point component detailpage
- Leaflet.map warning
- Remove gap in the sidebar demo
- Remove demo container flickering
- Missing adjustments of the tests and demos

### Documentation

- Rewrite documentation startpage 'index.md' with updated information

### Features

- Make image in the footer optional
- Add setting to make the navbar fixed at te top
- Add description on how to change the theme in the documentation
- Add {% load insight_tags %} to all demo containers
- Add customization page and remove customization section from component pages
- Add dedicated navbar context to navbar detailpage
- Update selected link in navbar
- Remove placeholder in code container
- Add new class for demo container scripts
- Rename 'card_horizontale' to 'app_card'
- Add line numbers and dark theme support to code block component
- Add git link to template and scripts file to demo container
- Apply main theme to demo containers
- Add global setting for navbar config 'fixed' and update default settings
- Add language and optional filename to code block
- Improve layout of the customization page
- Add new font Atkinson Hyperlegible for better a11y support
- Connect components via related topic section
- Improve a11y section on several component detailpages
- Replace clipboard.js with direct clipboard API call
- Remove clipboard.js and add integrity checks for third party JavaScript and CSS files
- Add parameter tables to component detailpages
- Add basic dockerfile
- Add ToC generation script

### Miscellaneous

- Delete unused stylesheet files

## [1.7.0] - 2026-01-12

### Features

- Add support for python 3.12 and 3.14

## [1.6.0] - 2025-12-11

### Documentation

- Add commercial licensing option and update ignore files

### Features

- Add image to the description section of the footer
- Add custom css class for input elements
- Use inline-tag class for multiselect tags
- Use input class for all components with an suitable input element

### Testing

- Remove assert for image-tag from the login page test

## [1.5.0] - 2025-12-03

### Bug Fixes

- Footer and table component

### Features

- Improve a11y for icon based buttons
- Improve tests for footer and table
- Improve input and select elements
- Extend form example
- Multiselect dispatch event on change
- Add accent color to checkbox and range slider
- Increase text size in table component

## [1.4.1] - 2025-11-28

### Bug Fixes

- Default value for maximal_checked of the checkbox_group component
- Missing renaming of id to tag_id in the radio_block component
- Adjust padding of the sidebar to match navbar
- Toggle component detailpage
- Htmx loading indicator
- Range slider progress in htmx requests
- Bottom padding of the sidebar

## [1.4.0] - 2025-11-27

### Bug Fixes

- Detailpages with more than one demo containers
- Rename id to tag_id for several components
- Typos

### Features

- Improve components and component detailpages
- Add iterm_per_page parameter to pagination method
- Rename radio component
- Add RTL support for range slider
- Add new input_field component
- Add input_field docu and detailpage
- Add initial check to checkbox_group and maximum checked restriction

### Testing

- Adjust test settings and add beautifulsoup4 to dependencies
- Add smoke tests for the component and storybook views
- Add tests for the checkbox, radio, toggle and slider component
- Add tests for the pagination

## [1.3.1] - 2025-11-25

### Bug Fixes

- Loading of the tailwind_cli tag

## [1.3.0] - 2025-11-24

### Bug Fixes

- Dependencies

### Documentation

- Add CONTRIBUTORS.md with project contributors
- Add tailwind-cli information

### Features

- Add switch to not use tailwind_cli tag

## [1.2.3] - 2025-11-20

### Bug Fixes

- Blank lines and remove makefile hook
- Template indentation and missing closing tags
- Lint settings
- Default SECRET_KEY
- Override staticfiles storage in test configuration
- Use STORAGES dict for Django 5.2 compatibility

## [1.2.2] - 2025-11-20

### Bug Fixes

- Align pre-commit hooks with template
- Align login tests with updated template

## [1.2.1] - 2025-11-20

### Bug Fixes

- Satisfy Ruff and test package layout for CI

### CI/CD

- Align workflows with insight-ci (no Docker)

## [1.2.0] - 2025-11-19

### CI/CD

- Update checkout and simplify release-develop

### Features

- Add integrable radio_group component
- Add labels to input components
- Add new select component
- Change height and gap settings for brand logo
- Add name property to toggle button and range slider
- Add defalt value to radio_group component
- Make loginform labels optional
- Add selected values option to checkbox and select component
- Make width of sidebar component customizable
- Add optional icon to sidebar title
- Add option to show radio_buttons and checkboxes in a row
- Add padding to sidebar and adjust title area
- Show filled track of range slider component
- Add id to radio_group component
- Add new component 'select'

### Miscellaneous

- Add CODEOWNERS and document ownership
- Refresh tooling and login template
- Tighten multiselect types and smoke docstring

### Testing

- Add smoke and integration examples
- Reorganize by test type

## [1.1.0] - 2025-11-17

### Documentation

- Add badges and dynamic version note
- Expand CI and tooling badges

### Features

- Add multiselect component
- Add JavaScript classes and improve browser logging
- Improve multiselect

## [1.0.0] - 2025-11-17

### Bug Fixes

- Korrigiere Pfad zur Index-Vorlage in views.py
- Erhöhe Intervall für Live-Inhalte auf 20 Sekunden
- Pfad der Template-Include auf components/table_view.html korrigieren
- Titel in base.html auf korrekten Dateinamen anpassen
- Korrigiere Titel, optimiere HTML-Struktur und lade JS modular in base.html
- Korrigiere Template-Pfad für Kartenansicht in toggle_view
- Schließe body-Tag korrekt in base.html ab
- Attribut selected in Sprachoptionen auf selected="selected" setzen
- Template für language_selector und Navbar-Brand-Rendering korrigieren
- Korrigiere den Template-Pfad im language_selector Decorator
- Theme-Toggle immer anzeigen, unabhängig vom Language-Selector
- Behebe Probleme mit HTML-Attributen und aktualisiere Skripte
- Onclick-Attribut aus toggle_theme.html entfernt und Debugging verbessert
- Entferne doppelte Deklaration von wsComponents in WebSocket-Logik
- Theme-toggle and toggle_view issue
- Live_content issue and remove alpine.js
- Sidebar issue
- Styles and temporarily use only tailwind
- Missing spacing in 'rtl'-mode
- Issues from feedback
- Linting and cleanup
- Issues related to tailwind update
- Navbar url and switch login buttons
- Dependencies in pyproject.toml
- Pyproject.toml order
- Move input.css outside static directory
- Path to font file
- Remove open-graph and twitter meta tags
- Template and font path in input.css
- Font path
- Tests
- Responsiveness and navbar
- Radio_group icon issue
- Linting
- Flip_card and 3D carousel
- Component demo issues
- Navbar issues
- Set fixed versions for some dependencies and set ruff python version
- Wrong parameter name

### Build System

- Füge pyproject.toml für Projektmetadaten hinzu

### CI/CD

- Align versioning with release-please

### Documentation

- Titel in index.html auf "Django Insight UI index.html" ändern
- Icons, and update of js lib, some other chore
- Websocket support component added
- Websocket is with version 2.0 directly available from htmx
- Add English translations and component screenshots

### Features

- Füge dev dependency group mit pytest dependencies hinzu
- Füge Komponenten für Formular-Fehler und -Erfolg hinzu
- Storybook-Komponente für Django Insight UI hinzufügen
- Ansicht zwischen Tabellen- und Kartenansicht per HTMX umschalten ermöglichen
- Füge Theme-Umschalter für Insight UI hinzu
- Füge Insight-UI Modal-Komponente hinzu
- Split main js into component javascript files
- Toggle between card and table views
- SVG-Icons für Bestätigung, Fehler, Beispiel, Info, Erfolg und Warnung hinzufügen
- Individual modals files to get to the point of atomic design ideas slowly
- Svg icons, done with an ai
- Toggle_theme
- System utility tools and live metrics for Insight UI Storybook, including a WebSocket-based server for real-time disk, memory, and system status monitoring.
- Favicon, SEO- und Social-Media-Meta-Tags sowie Utility-Script hinzufügen
- Sprachumschalter-Komponente in Insight UI hinzufügen
- Füge Tests für Insight UI Template Tags hinzu
- Theme-Toggle zur Navbar hinzufügen
- Füge detailliertes Logging für WebSocket-Initialisierung und Events hinzu
- Verbessere WebSocket-Komponente mit JSON-Verarbeitung und Styling
- WebSocket-Komponente mit verbesserter JSON-Verarbeitung aktualisieren
- WebSocket-Server sendet jetzt HTML-Fragmente für HTMX-Integration
- Füge detailliertes Debugging für WebSocket-Verbindung hinzu
- Füge robuste Prüfungen für HTMX und WebSocket-Extension hinzu
- Aktualisiere HTMX und WebSocket-Extension auf die neueste Version
- Standardize text colors
- Add carousel view
- Add pagination example
- Sidebar switches window side in rtl mode and add new manual opening sidebar variant
- Add searchbar
- Add toggle button and slider
- Add dark-mode variant for searchbar
- Add insight-ui settings to context-processor
- Add new card and component classes for buttons
- Make card parameters more felxible
- Make stylesheet path configurable
- Add dropdown-menu, user-menu, login-screen and improve navbar
- Add copyable code block
- Add image carousel
- Add config system
- Add django-tailwind-cli and update tailwind to v4.1
- Add icons to links and fix some issues
- Improve navbar mobile menu and add modal to navigation
- Improve image-carousel and cards image source
- Improve navbar configuration
- Add chat layout and improve code block component
- Improve docs
- Add icons to links in footer and navbar and improve infinite scroll
- Improve toggle_view, add radio-group component and fix some issues
- Improve sidebar
- Add updated sidebar.js
- Add query_params to breadcrumbs and radio_group
- Add filters and distribute components to individual pages
- Add geo and chart libraries and improve documentation
- Add tooltips and popovers
- Improve infinite scroll
- Add progress bars
- Improve dropdown, tooltip and popover components
- Add detailpage for every component
- Improve component inclusion
- Improve documentation of new components and improve charts and geo map component
- Improve accordion and 3D carousel component
- Improve demo-containers and fix design issues of several components
- Slightly improve documentation
- Improve generic_filter component
- Update navbar documentation
- Add query_params and push_url to generic_filter component
- Improve login screen
- Improve navbar brand logo themeing
- Make footer contact section customizable
- Make load third party javascript libraries configurable

### Miscellaneous

- Ignore files related to ai agents
- Replace tests with core as a main entry point
- Ändere Dateiberechtigungen für run_ui_tests.py
- Update localization files and dependencies
- Whitespace corrections
- Staticfiles should be collected with "python manage.py collectstatic"
- Fix errors, and dont get crazy
- Placeholder for additional functionality
- Placeholder for future use
- Removed own websocket implementation
- Added static
- Entferne den Theme-Toggle aus der Navbar
- Updates
- Add tailwind.config.js and new font 'Inter'
- Improve readme's
- Remove custom icons
- Remove unnecessary JavaScript files
- Remove unused dependecies
- Translate
- Adopt python 3.12 baseline
- **ci:** Add semantic-release workflow and dynamic versioning via hatch-vcs
- **python:** Bump baseline to 3.13 (tooling, CI, docs)
- Remove english documentation
- **ci:** Use 'develop' as prerelease branch; fix version fallback to 'insight-ui'

### Refactoring

- Vereinfache HTMX-Attribut-Rendering in HTML-Vorlagen
- Verbessere Barrierefreiheit und Struktur der Navigationsleiste
- Entferne Black aus dev-Abhängigkeiten
- Vereinfache Testfälle für Template-Tags und verbessere Typisierung
- URLs und Views für insight_ui anpassen und vereinfachen
- Storybook-Layout neu anordnen und Ansicht mit Umschalter hinzufügen
- Kern-Utilities aus insight-ui.js extrahieren und Komponenten entfernen
- Insight UI auf Storybook umstellen und HTMX-Extensions entfernen
- Payload-Generierung und Mapping in Klassen kapseln und verbessern
- Komponenten-Dateien umbenennen und Verweise anpassen
- Passe imports an und füge Logging in toggle_view hinzu
- Entferne unnötige Aktionen aus Demo-Modal in Storybook-Template
- SVG-Icons entfernen und Toggle-View-Komponenten verbessern mit Logging
- Modal-Komponenten in separate Dateien auslagern und Template bereinigen
- Entferne alte icons und vereinfache modale mit dynamischen icons und beschreibungen
- Entferne rechte Sidebar und passe Storybook-Pfad an
- Navbar, Sidebar und Footer in Blöcke umwandeln und überflüssigen Code entfernen
- ThemeToggle-Code vereinfachen und Kommentare bereinigen
- Lade statische Dateien und Sprachfunktionen im Sprachumschalter-Template
- WebSocket-Extension in insight-ui-htmx-extensions umbenennen und Logs anpassen

### Styling

- HTML-Attribute in toggle_view.html neu formatieren
- Korrigiere Übersetzungs-Strings und entferne unnötige Kommentare in Modal-Templates
- Brand-Logo-Platzhalter und Sprachselector im Navbar-Template verbessern
- Verbessere die Einrückung und Struktur im Navbar-Template
- Positioniere Branding links in der Navbar und zentriere Navigation
- Zentrale CSS-Klassen im WebSocket-Template angewendet und optimiert

### Testing

- Playwright-Browserpfad für lokale Entwicklungsumgebung aktualisieren
- Erstelle __init__.py für das Tests-Modul in insight_ui

---
*Generated by [git-cliff](https://git-cliff.org/)*
