# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- **config:** Retain copyright notice compatibility alias
- **package:** Ship documentation app in wheel

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

### Miscellaneous

- Regenerate minified assets
- **pre-commit:** Autoupdate hooks
- Regenerate minified stylesheet
- Regenerate minified stylesheet
- Regenerate minified assets
- Regenerate minified stylesheet
- Update stylesheet
- Regenerate minified stylesheet
- Regenerate minified stylesheet
- Regenerate minified assets
- Regenerate minified assets
- Regenerate minified assets
- Regenerate minified stylesheet
- **static:** Generate minified assets only in CI

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
- **sidebar:** Await drawer opening animation

## [1.12.0] - 2026-08-20

### Bug Fixes

- Correct various issues in the JavaScript components
- **static:** Preserve generated stylesheet newline
- **static:** Build complete CDN assets
- **deps:** Sync generated requirements with uv lock
- **container:** Refresh Debian security packages
- Use correct template for htmx swap of component detailpages
- Add alternating row colors for parameter tables again

### Documentation

- Add missing docstrings to JavaScript code
- Reorganize and cleanup developer documentation
- Remove 'assets' directory from developer documentation
- Update 'Documentation' part of the README
- Update readme
- Remove internal operations details

### Features

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

- Regenerate minified assets
- Update dependencies
- Update node dependencies
- Update pre commit hooks and fix linting
- Format websocket demo readme
- Regenerate minified stylesheet
- Fix uv.lock
- Regenerate minified assets
- **static:** Regenerate assets after rebase
- Regenerate stylesheet
- Regenerate minified assets
- Add --no-minify to rebuild stylesheet command
- **pre-commit:** Autoupdate hooks
- **pre-commit:** Autoupdate hooks

### Refactoring

- Change indentation mode from tabs to spaces for the 'tabs' and 'sidebar' script files
- Replace structlog with stdlib logging
- Remove old websocket demo subproject 'utils'

### Testing

- Add new tests for JavaScript components
- Move JavaScript tests to main tests directory
- Adjust tests for new accessibility
- Adjust tests and remove unnecessary css class checks

## [1.11.2] - 2026-07-21

### Bug Fixes

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

### CI/CD

- **static:** Guard Tailwind theme asset sync
- **cdn:** Publish release assets from release workflow
- **cdn:** Pin CDN version in GitOps updates

### Documentation

- **theme:** Document semantic motion roles
- **brand:** Align settings example with brand mark
- **deployment:** Use canonical insight ui develop host

### Features

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

### Miscellaneous

- Regenerate minified stylesheet
- **ignore:** Exclude playwright cli artifacts
- Fix merge issues
- Add pre-commit hook for checking used design tokens in templates
- Regenerate minified assets
- Mark check_design_tokens script as executable
- Regenerate minified styesheet
- Regenerate stylesheet
- Regenerate stylesheet
- Regenerate minified stylesheet
- Regenerate minified assets

### Refactoring

- Move html code for the search results to a separate template file
- Sort css classes in all templates
- Move 'layout' directory to components directory

### Testing

- Fix tests
- Fix tests
- Update JavaScript tests

## [1.11.0] - 2026-06-18

### Bug Fixes

- **ci:** Run container publish on every branch push
- **ci:** Pin only published container digests
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

### Build System

- **static:** Refresh generated tailwind asset

### CI/CD

- Migrate digest-pin to least-privilege app token
- **user-dropdown:** Refresh required checks

### Documentation

- **ci:** Refresh digest-pin token comment to app-token setup

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

### Miscellaneous

- **ci:** Retrigger repository policy after workflow promotion
- Regenerate minified assets
- Regenerate minified stylesheet
- Fix merge issues
- Regenerate minfied stylesheet
- **navbar:** Apply formatter output
- Linting
- Regenerate minified stylesheet
- Regenerate minified stylesheet
- Regenerate minified stylesheet
- Regenerate minified stylesheet
- Update stylesheet

### Refactoring

- Remove redundant loading of script files in base.html and components.html
- Reduce hardcoded index page tokens
- **theme:** Semantic range control tokens
- **brand:** Rename brand mark component
- Move type definitions to separate file

### Testing

- **forms:** Keep status include within line limit
- **theme:** Document shadow token checks
- **i18n:** Document container translation contract
- **i18n:** Avoid compiled catalog dependency
- Fix tests

## [1.10.2] - 2026-05-27

### Bug Fixes

- **navbar:** Position user dropdown below trigger

### Miscellaneous

- Release develop to main

## [1.10.0] - 2026-04-08

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
- **navbar:** Sync user dropdown position to develop
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

### CI/CD

- Automate release-please PR checks and merge
- **guard:** Preserve branch-policy check name
- **guard:** Preserve branch-policy check name
- **feature:** Mirror required legacy test checks
- Allow stacked branch pull requests
- Align blue/green container publish and promotion
- Use central reusable container workflow
- **container:** Enable manual django image builds
- **cdn:** Upload static assets by branch alias
- Use central reusable workflows

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
- **cdn:** Document static asset delivery

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
- Correct linting
- Merge develop into dataclasses branch
- Fix merge issues
- Normalize changelog whitespace
- Add missing __init__ files for new 'create_component' command
- Release insight-ui — sync develop→main (5 months of work)

### Refactoring

- Change toc generator indentation from two to four whitespaces
- Remove special parameter context handling from views.py
- Remove hardcoded list of components from smoke tests
- Rename 'table' and 'main' storybook
- Remove obsolete storybook template files
- Adopt logo component

### Reverted

- Get_component_demo_context() linter warning

### Styling

- Format pagination dataclass test

### Testing

- Improve smoke tests for storybooks and fix loginscreen test
- Use Component Enum Class for smoke tests
- Js tests
- Update tests to use dataclass based config system for the component tests
- Fix tests
- Split component tests into seperate files
- Apply django-upgrade header style

## [1.9.1] - 2026-02-24

### Bug Fixes

- Hide static docs sidebars on smaller viewports

### CI/CD

- Add changelog workflow from insight-ci template

### Miscellaneous

- **pre-commit:** Autoupdate hooks
- **develop:** Release 1.9.1

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

- **pre-commit:** Autoupdate hooks
- Pin and update all dependencies
- **docs:** Remove completed architecture guide documents
- **docs:** Remove obsolete index.md and fix README links
- **develop:** Release 1.9.0

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

### Wip

- Feat: add context files for component detailpages and add new detailpage template
- Feat: add support for sorting to table component

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

- **pre-commit:** Autoupdate hooks
- Delete unused stylesheet files
- **develop:** Release 1.8.0

## [1.7.0] - 2026-01-12

### Features

- Add support for python 3.12 and 3.14

### Miscellaneous

- **pre-commit:** Autoupdate hooks
- **pre-commit:** Autoupdate hooks
- **develop:** Release 1.7.0

## [1.6.0] - 2025-12-11

### Documentation

- Add commercial licensing option and update ignore files

### Features

- Add image to the description section of the footer
- Add custom css class for input elements
- Use inline-tag class for multiselect tags
- Use input class for all components with an suitable input element

### Miscellaneous

- **pre-commit:** Autoupdate hooks
- **develop:** Release 1.6.0

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

### Miscellaneous

- **pre-commit:** Autoupdate hooks
- **develop:** Release 1.5.0

## [1.4.1] - 2025-11-28

### Bug Fixes

- Default value for maximal_checked of the checkbox_group component
- Missing renaming of id to tag_id in the radio_block component
- Adjust padding of the sidebar to match navbar
- Toggle component detailpage
- Htmx loading indicator
- Range slider progress in htmx requests
- Bottom padding of the sidebar

### Miscellaneous

- **develop:** Release 1.4.1

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

### Miscellaneous

- **develop:** Release 1.4.0

### Testing

- Adjust test settings and add beautifulsoup4 to dependencies
- Add smoke tests for the component and storybook views
- Add tests for the checkbox, radio, toggle and slider component
- Add tests for the pagination

## [1.3.1] - 2025-11-25

### Bug Fixes

- Loading of the tailwind_cli tag

### Miscellaneous

- **develop:** Release 1.3.1

## [1.3.0] - 2025-11-24

### Bug Fixes

- Dependencies

### Documentation

- Add CONTRIBUTORS.md with project contributors
- Add tailwind-cli information

### Features

- Add switch to not use tailwind_cli tag

### Miscellaneous

- **main:** Release 1.2.2
- Merge main into develop to resolve conflicts
- **pre-commit:** Autoupdate hooks
- **develop:** Release 1.3.0

## [1.2.3] - 2025-11-20

### Bug Fixes

- Blank lines and remove makefile hook
- Template indentation and missing closing tags
- Lint settings
- Default SECRET_KEY
- Override staticfiles storage in test configuration
- Use STORAGES dict for Django 5.2 compatibility

### Miscellaneous

- **develop:** Release 1.2.3

## [1.2.2] - 2025-11-20

### Bug Fixes

- Align login tests with updated template

### Miscellaneous

- **develop:** Release 1.2.2

## [1.2.1] - 2025-11-20

### Bug Fixes

- Align pre-commit hooks with template
- Satisfy Ruff and test package layout for CI

### CI/CD

- Align workflows with insight-ci (no Docker)

### Miscellaneous

- **develop:** Release 1.2.1

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
- **develop:** Release 1.2.0

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

### Miscellaneous

- **develop:** Release 1.1.0

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
- Ruff format
- Ruff format
- Ruff format
- Ruff format
- Ruff format
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
- Linting
- Remove custom icons
- Remove unnecessary JavaScript files
- Remove unused dependecies
- Translate
- Adopt python 3.12 baseline
- **ci:** Add semantic-release workflow and dynamic versioning via hatch-vcs
- **python:** Bump baseline to 3.13 (tooling, CI, docs)
- Remove english documentation
- **ci:** Use 'develop' as prerelease branch; fix version fallback to 'insight-ui'
- **develop:** Release 1.0.0

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

### Aider

- Feat: Initialisiere Django Insight UI Projektstruktur
- Chore: korrigiere Konfiguration in pyproject.toml
- Basierend auf den Diffs und den erstellten Dokumentationsdateien sehe ich, dass Sie eine umfassende Dokumentationsstruktur für Django Insight UI erstellt haben. Die Dokumentation umfasst verschiedene wichtige Aspekte wie Installation, Schnellstart, Komponenten, Anpassung, Barrierefreiheit, Internationalisierung und Beitragsrichtlinien.
- (no commit message provided)
- (no commit message provided)
- Chore: Hatchling-Konfiguration für Paketbuild hinzufügen
- Ich sehe, dass die Dateien erfolgreich erstellt wurden. Hier ist ein Commit-Vorschlag für diese Änderungen:
- Feat: Füge Template Tags für alle UI-Komponenten hinzu
- Refactor: Erweitere Template-Tag-Tests für umfassende Abdeckung
- Die Änderungen sehen sehr gut aus! Ich habe die Dateien `insight_ui/static/insight_ui/css/insight-ui.css` und `insight_ui/static/insight_ui/js/insight-ui.js` überprüft und beide Implementierungen sind vollständig und robust.
- Basierend auf den Änderungen generiere ich einen passenden Commit-Nachricht:
- Feat: Implementiere dynamische Sprachauswahl mit JavaScript-Formular
- Feat: Verbessere Sprachauswahl-Logik mit CSRF-Token-Handling
- Feat: integriere TailwindCSS CDN und erweiterte HTMX-Funktionalität
- Feat: integriere TailwindCSS und django-htmx für moderne UI-Komponenten
- Refactor: Verbessere Lesbarkeit des HTMX-Formulartemplates durch Zeilenumbrüche
- Feat: Integriere django-htmx Middleware und TailwindCSS CDN
- Refactor: Verbessere Lesbarkeit der HTMX-Attribute in Form-Template
- Refactor: HTMX-Attribute in einer Zeile für bessere HTML-Kompatibilität formatieren
- Refactor: Verbessere Lesbarkeit der HTMX-Attribute in Form-Template
- Feat: Zentralisiere TailwindCSS und HTMX im Base-Template
- Refactor: HTMX-Attribute in einer Zeile formatieren
- Refactor: Verbessere Lesbarkeit der HTMX-Attribute in Form-Template
- Refactor: HTMX-Attribute in einer Zeile formatieren
- Refactor: Umbenennung von "tests" zu "core" in Projektstruktur
- Refactor: Ersetze WSGI durch ASGI in Django-Konfiguration
- Feat: Konfiguriere Template-Verzeichnis und füge i18n-Kontextprozessor hinzu
- Fix: Lade i18n und andere Template-Tags am Anfang des HTML-Dokuments
- Feat: Playwright-Tests für Django Insight UI hinzufügen
- Fix: Korrigiere Regex-Syntax in Playwright-Test für Modal-Klasse
- Fix: Playwright-Konfiguration in pytest.ini korrigieren
- Feat: Konfiguriere Django und Playwright für UI-Tests
- Feat: Konfiguriere Playwright-Tests für Firefox und verbessere Browser-Einstellungen
- Chore: Playwright-Konfiguration für besseres UI-Testing anpassen
- Feat: Standalone Playwright-Tests für Django Insight UI hinzufügen
- Fix: Behebe Scope-Mismatch und verbessere Playwright-Test-Konfiguration
- Test: Verbessere Playwright-Test mit detaillierter Fehlerbehandlung und Debugging
- Ich sehe, dass Sie die Playwright-Tests entfernt haben. Das ist eine gute Entscheidung, da die Browser-Installation problematisch war.
- Fix: Testfälle an aktuelle Template-Implementierung anpassen
- Feat: WhiteNoise und STATIC_ROOT zu Django-Einstellungen hinzufügen
- Feat: Tailwind CSS Integration mit Dark Mode und Custom Theme verbessern
- Refactor: Sprachauswahl-Komponente mit robustem CSRF-Token-Handling verbessern
- Fix: Korrigiere Sprachauswahl-Template ohne optionale ID und mit korrekter Sprachvergleichslogik
- Fix: Korrigiere Sprachauswahl mit LANGUAGE_CODE statt current_language
- Fix: Sprachauswahl-Funktionalität durch CSRF-Token-Verbesserung korrigieren
- Fix: CSRF-Token-Handling und Fehlerbehandlung in Sprachauswahl verbessern
- Feat: Navbar-Sprachauswahl direkt integrieren und Sprachwechsel-Funktion globalisieren
- Feat: Globale Sprachwechsel-Funktion für Navbar hinzufügen
- Feat: Integriere HTMX-Views und Komponenten-Routing in core/urls.py
- Feat: Erstelle Views für Insight UI Komponenten
- Refactor: Verbessere JavaScript für Sprachwechsel-Funktion
- Feat: Implementiere robuste CSRF-Token-Erkennung für Sprachauswahl
- Feat: Verbessere Sprachauswahl-Mechanismus mit robustem CSRF-Token-Handling
- Feat: Verbessere CSRF-Token-Handling für Sprachauswahl und JavaScript
- Fix: CSRF-Token-Handling in Templates und JavaScript verbessern
- Fix: CSRF-Token-Debugging und Meta-Tag-Formatierung korrigieren
- Refactor: CSRF-Konfiguration für HTMX-Formulare verbessern
- Refactor: Verbessere Lesbarkeit der HTMX-Attribute im Formular-Template
- Fix: Korrigiere HTMX-Template-Tags in Formular-Komponente
- Refactor: CSRF-Schutz für HTMX-Formulare aktivieren
- Feat: Theme-Toggle für TailwindCSS und bessere Icon-Darstellung optimieren
- Feat: Playwright-Tests für Theme-Toggle-Funktionalität hinzufügen
- Feat: Theme-Toggle-Button mit korrekter CSS-Klasse versehen
- Feat: Sprachauswahl-Bedingung in Navbar-Template korrigieren
- Fix: Entferne doppelte i18n-Ladeanweisung in Navbar-Template
- Feat: Dark Mode Switch und Sprachauswahl in UI korrigieren
- Refactor: Entferne doppelte Sprachauswahl im Hauptinhalt
- Feat: Sprachauswahl in Navbar mit Django-Fallback implementieren
- Refactor: Entferne `options`-Referenzen in Navbar-Vorlage
- Feat: Sprachauswahl-Funktionalität in der Navbar korrigieren
- Fix: Sprachauswahl-Template-Tag in Navbar korrigiert
- Feat: Sprachauswahl in Navbar mit Django-Formular implementieren
- Fix: Korrigiere Sprachauswahl-Logik in der Navbar-Komponente
- Feat: Sprachauswahl in Navbar mit Fallback-Optionen verbessern
- Fix: Korrigiere Formatierung der Sprachauswahl-Optionen in der Navbar
- Style: Korrigiere Formatierung der Sprach-Auswahl-Option
- Feat: Dark Mode Switch in Navbar immer sichtbar hinzufügen
- Feat: Dark Mode Switch in Navbar hinzufügen
- Refactor: Entferne doppelten Dark Mode Switch in der Navbar
- Refactor: Sprachauswahl in separate Komponente auslagern
- Refactor: Komponenten in separate Dateien ausgelagert und Base-Template umstrukturiert
- Feat: Modal-Schließfunktionalität über X, Abbrechen und Backdrop hinzufügen
- Feat: Modal-Dialoge für verschiedene Nachrichtentypen hinzufügen
- Feat: Modal-Dialoge in Storybook-Seite hinzufügen und erweitern
- Feat: Async-Logging für HTMX-Kontaktformular implementieren
- Feat: Implementiere HTMX-Formular-Rückleitung zur Storybook-Seite
- Fix: HTMX-Formular mit korrekter Konfiguration und Zielbereich aktualisieren
- Fix: Korrigiere Kommentar für erfolgreiche Formularantwort
- Fix: Korrigiere HTMX-Formular-Attribute für korrekte Datenübertragung
- Fix: Korrigiere HTMX-Attribut-Syntax in Formular-Template
- Refactor: Korrigiere HTMX-Attribute und Formular-Template-Syntax
- Feat: Verbessere HTMX-Formular-Handling mit Debug-Logging und manueller Formularstruktur
- Feat: Synchrone Formular-View mit detailliertem Logging hinzufügen
- Feat: Synchrone Formular-Verarbeitung mit Logging hinzufügen
- Fix: Unterstütze POST-Requests auf der Startseite
- Fix: Korrigiere Einrückungsfehler in core/urls.py und füge i18n_patterns korrekt hinzu
- Feat: Formular-Erfolgsmeldungen und Fehler im Index-Template hinzufügen
- Refactor: Kontextbereitstellung und Formular-Rendering in Views verbessern
- Feat: Debugging-Ausgaben für Formular-Logging hinzufügen
- Feat: Logging-Ausgaben für HTMX-Formulare mit Print-Statements hinzufügen
- Feat: Sidebar mit Ein- und Ausfahren und Hover-Funktionalität hinzufügen
- Fix: Seitenleisten-Toggle-Button in Navbar mit korrekter ID hinzufügen
- Refactor: Debug-Ausgaben für Sidebar-Toggle-Button hinzufügen
- Style: Layout-Verbesserungen für Sidebar und Hauptinhalt optimieren
- Refactor: Layout der Demo-Sektionen optimieren und zentrieren
- Feat: Rechte Sidebar mit Ein- und Ausblenden implementieren
- Fix: Ersetze ungeschütztes Ampersand durch HTML-Entität in base.html
- Fix: Rechte Sidebar-Verhalten und Styling korrigieren
- Feat: Linke Sidebar mit Ein- und Ausblenden implementieren
- Feat: Linke Sidebar mit Swipe-Funktionalität und Escape-Taste verbessern
- Refactor: Sidebar-Interaktion mit Hover-Bereichen und Navbar-Buttons umgestalten
- Refactor: Sidebar-Funktionalität mit Hover-Verhalten aktualisieren
- Feat: Linke Sidebar mit verbessertem Hover und Zustandsspeicherung
- Refactor: Sidebar-Hover-Verhalten und Styling verbessern
- Feat: Playwright-UI-Tests für Sidebar, Responsivität und Modalfunktionen hinzufügen
- Chore: Playwright-Tests für global installierte Version anpassen
- Fix: Playwright-Konfiguration für UI-Tests aktualisieren
- Fix: Korrigiere Playwright-Testausführung mit pytest in run_ui_tests.py
- Ich schlage vor, die Playwright-Tests zu deaktivieren und stattdessen eine einfache Meldung auszugeben, dass die Tests deaktiviert sind. Hier sind die notwendigen Änderungen:
- Refactor: Entferne globale Playwright-Referenz in Testdatei
- Chore: Sidebar-Komponenten in separate Templates aufteilen
- Feat: Sidebar-Autoslide mit manueller Steuerung hinzufügen
- Feat: Heroicons SVG-Zahnrad-Icon in Navbar ersetzen
- Feat: Implementiere automatisches Ausblenden der linken Sidebar bei Mausabstand
- Refactor: Vereinheitliche Sidebar-Logik für linke und rechte Seitenleiste
- Refactor: Linke Sidebar vollständig entfernen
- Refactor: Linke Sidebar entfernen und Layout anpassen
- Fix: Implementiere Funktionalität für X-Button in rechter Sidebar
- Refactor: X-Button aus der rechten Sidebar entfernen
- Feat: Schließen-Button zur rechten Sidebar hinzufügen
- Fix: Sidebar-Schließen-Button korrigieren, um immer zu funktionieren
- Fix: Sidebar-Schließen-Button-Logik verbessern und Debugging hinzufügen
- Fix: Fehlerbehandlung für closest-Methode in Event-Listener hinzufügen
- Refactor: Fehlerbehandlung und Performance für Event-Listener verbessern
- Refactor: Schließen-Button in Sidebar an untere linke Ecke verschieben
- Fix: Sidebar-Schließen-Button debuggen und Überfluss-Scroll hinzufügen
- Fix: Sidebar-Klassen korrekt beim Öffnen und Schließen verwalten
- Refactor: Entferne Debug-Konsolenausgaben aus JavaScript-Code
- Refactor: Umbenennung von demo_sections.html zu storybook.html
- Style: Verbessere Storybook-Container-Layout für Responsivität
- Refactor: Sidebar-Link und Zahnrad-Icon aus Navbar entfernen
- Refactor: Bereinige pyproject.toml von veralteten Konfigurationen
- Fix: Ruff-Konfiguration in pyproject.toml aktualisieren
- Die Änderungen sehen gut aus. Hier sind noch ein paar zusätzliche Empfehlungen für die Teststruktur:
- Chore: Ersetze assert-Anweisungen durch pytest-Erwartungen in Testdateien
- Fix: ARIA-Attribute für bessere Barrierefreiheit in Modal- und Formular-Komponenten ergänzen
- Fix: entferne doppelte Überschrift "Willkommen bei Django Insight UI" im Index-Template
- Fix: Dark Mode Toggle in base.html implementieren und Icons korrekt wechseln lassen
- Style: Navbar mit Benutzer-Icon ergänzen und Navigation optisch ausbalancieren
- Refactor: Verschiebe Brand-Element in der Navbar nach rechts
- Refactor: JavaScript aus index.html in separate Datei insight-ui.js auslagern
- Fix: Korrigiere Aria-Attribut-Update in Navbar-Komponente auf String-Wert
- Refactor: Alle insight_ui URL-Aufrufe in insight_ui/urls.py auslagern
- Fix: URLs in core und insight_ui korrekt einbinden und importieren
- Fix: hx-target und hx-swap Attribute im switchable-view div in storybook.html ergänzen
- Feat: Komponente für Tabellenansicht mit Beispiel-Tabelle hinzufügen
- Fix: Pfad zum Template components/table_view.html in storybook.html korrigieren
- Fix: Umschalten zwischen Tabellen- und Kartenansicht in Storybook aktivieren
- Fix: hx-boost-Attribut zu Ansicht wechseln Buttons hinzufügen
- Fix: Ansicht wechseln Buttons korrekt auf Tabellen- oder Kartenansicht setzen
- Feat: Neue Templates für Karten- und Tabellenansicht hinzufügen
- Fix: Verhindere erneutes Umschalten und deaktiviere aktuellen Ansichtsknopf
- Fix: hx-trigger für Buttons nur setzen, wenn Ansicht nicht aktuell ist
- Fix: hx-trigger um "changed delay:500ms" für View-Switch-Buttons ergänzen
- Fix: Ladeindikator zu Ansicht-Buttons bei Wechsel hinzufügen
- Refactor: Zentralen JavaScript-Code in Komponenten aufteilen und Sidebar-Logik korrigieren
- Fix: Schließen-Button zum Schließen der Sidebar funktionsfähig machen
- Refactor: EventListener für right-sidebar-close in zentrale JS-Datei verschieben
- Refactor: Sidebar-JavaScript in extra_scripts Block auslagern und Inline-Skript entfernen
- Fix: Sidebar-Funktionalität durch Korrektur der Event-Listener wiederherstellen
- Fix: Dark Mode Umschalter mit Speicherfunktion und Eventlistener implementieren
- Fix: data-theme-toggle Attribut zum Dark Mode Button hinzufügen
- Refactor: Verschiebe den UI-Modus-Umschalter in eine separate Template-Datei
- Fix: setze data-theme Attribut beim Umschalten des Themes im Toggle-Button
- Fix: Modal-Komponenten per include statt custom tag einbinden für korrekte Anzeige
- Fix: if-Bedingungen in Buttons für aktuelle Ansicht lesbarer formatieren
- Fix: style-Attribut in Buttons für aktuelle Ansicht korrekt einfügen
- Fix: Schließen-Button der Benachrichtigung funktioniert jetzt korrekt
- Fix: Modal-Dialoge öffnen und schließen korrekt implementieren
- Fix: Schließen-Buttons im Modal korrekt mit Event-Listenern versehen
- Fix: Modals durch Setzen von display:block beim Öffnen sichtbar machen
- Feat: neue Sprach-JS-Datei und HTML-Komponente für Sprachumschaltung hinzufügen
- Fix: Sprach-JS in base.html einbinden und doppelte Storybook-Sprache entfernen
- Refactor: Typannotationen in insight_tags.py für bessere Lesbarkeit ergänzen
- Feat: zeige Sidebar beim Annähern der Maus an den rechten Rand an
- Fix: Schließen des Modals auf display:none statt hidden umstellen
- Fix: extrahiere Formulardaten als Strings statt Listen für Validierung
- Fix: füge data-insight-sidebar Attribut zur rechten Sidebar hinzu
- Refactor: gemeinsame Datenstruktur für Karten und Tabelle in toggle_view nutzen
- Refactor: gemeinsame payload für Karten- und Tabellendarstellung eingeführt
- Feat: füge Hilfsfunktionen für zufällige Payload-Generierung und Mapping hinzu
- Fix: gleiche Tabellenüberschriften wie Kartenattribute verwenden
- Feat: kürze content in Tabelle auf 10 Zeichen mit ... am Ende
- Fix: fülle Tabelle in Toggle-View initial mit Daten
- Fix: Fehler bei Toggle-View beheben durch korrekte DataMapper-Aufrufe verwenden
- Fix: initiale Toggle-View-Daten im Index-Template an Storybook-Include übergeben
- Fix: Toggle-View im Storybook mit korrekten Daten und Ansicht initialisieren
- Fix: Logger in views.py definieren, um Fehler bei toggle_view zu beheben
- Refactor: SVG-Inhalte aus HTML auslagern und per include einbinden
- Fix: behebe fehlenden Zeilenumbruch am Ende von toggle_view.html
- Refactor: SVG-Inhalte in einzelne Dateien auslagern und Verweise anpassen
- Refactor: SVG-Icons in eigene Dateien auslagern und in storybook.html referenzieren
- Fix: Tippfehler in modal.html korrigieren und Kommentar verbessern
- Fix: Tippfehler in storybook.html korrigieren und Template-Tags laden
- Fix: Pfad zum SVG-Icon im Modal-Template korrigieren
- Fix: Lade static-Tag in modal_demo.html zur Behebung von TemplateSyntaxError
- Fix: IDs in Modal-Templates an data-insight-target-Attribute angleichen
- Chore: Sprachwahl im Navbar-Template aktivieren und Sprachkontext im Index laden
- Fix: Sprachwahl im Navbar-Template mit korrekten Sprachvariablen ergänzen
- Fix: entferne doppelte Sprachvariablen in Navbar-Sprachauswahl-Template
- Fix: Sprachwahl im Navbar-Template korrekt initialisieren und anzeigen
- Feat: show_language_selector im navbar Template-Tag auf True setzen und Sprachen verfügbar machen
- Fix: show_language_selector im navbar Template-Tag auf True setzen und Sprachen verfügbar machen
- Fix: entferne doppeltes Argument show_language_selector in navbar-Funktion
- Refactor: Sprache wechseln via Formular und View mit HTMX-Unterstützung implementieren
- Fix: Sprachwahl im Template durch Laden der Sprachvariablen korrigieren
- Fix: entferne doppelte Sprachvariablen im Sprachselector-Template
- Fix: Sprachwahl im Template mit korrekten Sprachvariablen versehen
- Fix: Sprache im Dropdown korrekt wechseln und Deutsch als Default ohne Sprachcode anzeigen
- Fix: entferne doppelte Sprachvariablen im Sprachselector-Template
- Fix: Sprache ändern auf asynchrone Funktion umstellen statt Formularabsendung
- Fix: Formular beim Sprachwechsel korrekt absenden statt JavaScript-Funktion aufrufen
- Refactor: Sprache-Auswahl in eigene JS-Datei auslagern und Konsistenz herstellen
- Refactor: Lade verfügbare Sprachen in View und nutze sie im Template
- Fix: Sprache ändern Funktion auf benutzerdefinierte Methode umstellen
- Fix: Formular beim Sprachwechsel korrekt absenden statt JavaScript-Funktion aufrufen
- Refactor: set_language-View entfernen und Django-Standard für Sprachwechsel nutzen
- Fix: undefined name 'request' in insight_ui/views.py beheben
- Fix: ersetze eigene Sprachwechsel-URL durch Django-Standard i18n/setlang/
- Fix: max-width der Navbar von 7xl auf 6xl reduzieren für mehr Abstand
- Fix: utils im InsightUI-Objekt korrekt initialisieren und Fehler beheben
- Fix: setze data-theme Attribut im ThemeToggle für Storybook-Kompatibilität
- Fix: Theme-Toggle für Storybook und SSR mit data-theme Attribut korrigieren
- Fix: setze data-theme auf <html> statt <body> für funktionierenden Theme-Toggle
- Fix: Theme-Toggle für alle Buttons initialisieren und Event-Bubbling verhindern
- Fix: Console-Log beim Klicken des Theme-Toggle-Buttons hinzufügen
- Fix: Logs für Theme-Toggle Button Klicks zur Fehlerdiagnose hinzufügen
- Fix: Leerzeichen vor selected-Attribut im Sprachwahl-Option-Tag korrigieren
- Refactor: SVG-Icon in navbar.html in eigene Datei auslagern und einbinden
- Fix: Entferne überflüssiges Attribut in Sprachwahl-Option im Navbar-Template
- Fix: Attribut selected im Sprachwahl-Option-Tag korrekt setzen
- Fix: Entferne überflüssiges selected-Attribut in Sprachwahl-Optionen im Navbar-Template
- Refactor: entferne doppelte Sprachselector-Abschnitte in navbar.html
- Fix: setze selected-Attribut korrekt im Sprachwahl-Dropdown im Navbar-Template
- Fix: Entferne überflüssiges Attribut in Sprachwahl-Option im Navbar-Template
- Refactor: nutze toggle_language.html in navbar.html für Sprachunterstützung
- Feat: WebSocket-Komponente in Templates und JS für neue Seiten hinzufügen
- Refactor: WebSocket-Tag und Routine als eigene Inclusion-Tag in insight_tags.py auslagern
- Refactor: entferne WebSocket-Handling aus htmx-extension und behalte nur HTMX-Features
- Refactor: WebSocket-Komponente auf HTMX-Extension umstellen
- Feat: WebSocket-Unterstützung als HTMX-Extension hinzufügen und auto-initialisieren
- Fix: JSON-Daten im WebSocket-Frontend als formatierten Codeblock anzeigen
- Feat: Logging bei WebSocket-Nachrichten zum Debuggen hinzufügen
- Refactor: benenne WebSocket-Output-Div in insight-websocket-output um im Template
- Fix: Prüfe WebSocket-Nachricht auf gültiges JSON und logge Fehler im JS
- Fix: JSON-Darstellung als Text formatieren, um [object Object] zu vermeiden
- Refactor: ersetze 'websocket' durch 'insight-websocket' zur Vermeidung reservierter Begriffe
- Refactor: WebSocket-Komponente auf htmx v2 ws-Extension umstellen und Template-Tag anpassen
- Fix: Fehler bei getAttribute prüfen und nur bei Elementen WebSocket initialisieren
- Refactor: eigene WebSocket-Extension entfernen und offizielle htmx ws-Extension nutzen

### Merge

- Resolve conflicts (pyproject dynamic versioning; drop removed English doc)

### Wip

- Fix: responsiveness issues
- Feat: add detailpages for all components
- Feat: improve detailpage handling
- Feat: extend component detailpages
- Feat: add missing doc pages
- Chore: cleanup includes and css-tags
- Feat: add new components tabs, accordion and 3D carousel
- Fix: issues of new components
- Feat: improve documentation and component detailpages
- Feat: improve docs and component detailpages

---
*Generated by [git-cliff](https://git-cliff.org/)*
