# Changelog

All notable changes to **EET Calculator** are documented in this file.

The latest version appears first.

## [1.23] - 2026-08-01

### Added

- Added direct calculation recall through the `/api/calculation/<calculation_id>` route.
- Added the `/api/calculations/check` API allowing timing software to synchronize local Calculation Keys with the server.
- Added automatic reporting of the implemented **EEP protocol version** and **EET Calculator version** in every EEP JSON response.

### Changed

- Calculation recalls now preserve the Calculation Key in the Web interface.
- Improved interoperability between EET Calculator and external timing software implementing the EEP protocol.
- Improved robustness of Calculation Key handling.
- Improved robustness of Calculation Key recall and synchronization.

### Fixed

- Fixed handling of empty Calculation Key URLs (`/api/calculation/`).

### Validation

Validated the following scenarios:

- JSON A import.
- JSON B import.
- Direct recall by Calculation Key.
- Calculation synchronization API.
- Automatic version reporting.
- PDF generation after recalled calculations.
- Deployment validation on Ubuntu Server (OVH) using Gunicorn and Nginx.
- Version compatibility checks with external timing software.

---

## [1.22] - 2026-07-26

### Changed

- Refactored the management of the working document and user session.
- Fully separated Web and JSON workflows.
- The displayed working document is now independent from the Web calculation history.
- Web calculations now maintain a two-entry history to support the **Swap** function.
- JSON calculations (imports, Calculation Key recalls and searches) no longer modify the Web calculation history.
- The **Clear** function now resets only the working document without deleting the Web calculation history.

### Architecture

- Clarified the responsibilities of:
  - `WORK_DOCUMENT`: currently displayed document.
  - `CURRENT_CALCULATION`: latest Web calculation.
  - `PREVIOUS_CALCULATION`: previous Web calculation.
- JSON calculation documents continue to be stored permanently.
- Simplified session management.
- Removed obsolete debugging code.

### Validation

Validated the following scenarios:

- Successive Web calculations with swapping between the two latest calculations.
- JSON import followed by creation of a new calculation.
- Calculation recall using a Calculation Key.
- Search for a previously stored calculation.
- Simultaneous use of Web and JSON workflows without interference.

---

## [1.21] - 2026-07

### Added

- Added public search by Calculation ID.
- Added retrieval of an existing calculation for editing.
- Introduced automatic PDF generation adapted to the current context:
  - anonymized reports for public consultation;
  - identified reports when recalling a calculation.

### Changed

- Completed the architecture based on `RACE_SCHEMA` (exchange protocol) and `RACE_MODEL` (business model).
- First implementation compliant with the EEP 1.0 exchange protocol.
- Clarified the responsibilities of the business services, data model and PDF generation.
- Improved session handling for working documents.

### Fixed

- Corrected several edge cases when recalling stored calculations.
- Added explicit user feedback for unknown Calculation IDs.
- Improved robustness when accessing stored calculations in read-only mode.
- Fixed various minor workflow and user interface issues.

### Validation

- Validated the application under Windows.
- Validated deployment under Ubuntu Linux using Gunicorn and nginx.
- Validated calculation, public search, calculation recall, PDF generation and session management workflows.

---

## [1.20] - 2026-07

### Added

- Introduced the `document.py` business model.
- Established the business document as the central data structure used throughout the application.

### Changed

- Separated the business model from the user interface and calculation services, laying the foundation for the current application architecture.

---

## [1.10] - 2026-06

### Changed

- Performed a complete architectural refactoring.
- Simplified `app.py`.
- Centralized application configuration in `config.py`.
- Improved code readability and maintainability.
- Harmonized source code comments and documentation.
- Removed obsolete code and unused imports.

### Added

- Introduced `services/eet_calculator.py`.
- Introduced `services/formulaire.py`.
- Introduced `services/views.py`.
- Introduced `pdf.py`.
- Established a clear separation between routes, business services and views.

### Documentation

- Added a developer-oriented `README.md`.
- Updated the installation and deployment guide.

---

## [1.09a] - 2026-06

### Changed

- Standardized the grammatical gender of **EET** in all French documentation and user interface texts.

---

## [1.09] - 2026-06

### Added

- Added a contact address to the **About** page.

---

## [1.08b] - 2026-06

### Changed

- Harmonized HTML page titles across the application.
- Improved search engine optimization (SEO):
  - Added Open Graph metadata.
  - Added canonical URLs to all pages.
  - Improved multilingual page descriptions.
- Standardized page titles in French, English and German.
- Improved the **About** page.
- Updated the online documentation and help pages.
- Added recommendations regarding the use of timing data from the secondary timing system when available.
- Improved several German translations.
- Applied various minor user interface improvements.

### Fixed

- Corrected the display of several help pages.
- Fixed inconsistencies in labels and translation keys.
- Improved consistency of generated PDF reports across all supported languages.

### Added

- Added a dedicated maintenance page in preparation for future developments.

---

## [1.08a] - 2026-06

### Added

- Added automatic browser language detection.
- Added automatic support for French, English and German.
- Preserved the selected language in the user session.
- Added automatic fallback to English for unsupported languages.

---

## [1.08] - 2026-06

### Changed

- Added a default HTML title for the home page.
- Improved HTML titles for secondary pages.
- Improved search engine optimization (SEO).
- Introduced versioning for JavaScript resources.

---

## [1.07] - 2026-06

### Fixed

- Improved the robustness of form processing.
- Fixed an issue that could cause an HTTP 500 error when handling incomplete or malformed POST requests.

### Changed

- Introduced versioning for JavaScript resources.

### Added

- Prepared the application for search engine indexing.

---

## [1.05] - 2026-06

### Added

- Introduced a **Time Calculator** allowing users to calculate:
  - race time from start and finish times;
  - finish time from start time and race time;
  - start time from finish time and race time.
- Added independent precision settings for Time of Day (TOD) and race times.
- Added automatic formatting of times and durations during data entry.
- Added validation of start and finish times.
- Added validation of race duration inputs.

### Changed

- Preserved precision settings while navigating between the calculator and its help pages.
- Improved data entry ergonomics on desktop, tablet and smartphone.
- Harmonized validation and error messages with the EET Calculator.

### Calculation

- All calculations are performed with microsecond precision.
- Calculated race times are **truncated** to the selected precision and are never rounded.

### Documentation

- Added a dedicated help page for the Time Calculator.
- Translated the calculator and its documentation into French, English and German.

---

## [1.03] - 2026-06

### Fixed

- Added versioning to `base.html` to ensure JavaScript resources are reloaded after updates.
- Improved verification of user error messages.

---

## [1.02] - 2026-06

### Added

- Introduced calculation history with persistent storage of the current and previous calculations.
- Added the **Previous Calculation** panel to the results area.
- Added the **Reload** function to instantly switch between the two most recent calculations.
- Preserved calculation history after page reloads and browser restarts.
- Added the `update.sh` script to simplify application updates on Ubuntu and Debian.

### Changed

- Improved the robustness of Flask session management.
- Improved PDF document metadata.
- Updated the Ubuntu/Debian deployment documentation.

### Fixed

- Corrected the display of the previous calculation after successive calculations.
- Fixed preservation of the selected language after page reloads.
- Corrected language selector behavior.
- Fixed calculation history preservation when changing language.
- Stabilized user session handling.
- Removed temporary debugging traces.

### Validation

- Validated EET calculation.
- Validated PDF generation.
- Validated multilingual support.
- Validated previous calculation history and reload workflow.
- Validated repeated switching between the two latest calculations.
- Validated browser session persistence.
- Validated deployment on Ubuntu with Gunicorn and systemd.

---

## [1.01] - 2026-06

### Added

- Added automatic storage of the latest calculation in the user session.
- Added support for the previous calculation.
- Introduced the **Reload** function to switch between the two latest EET calculations.
- Added persistent user sessions with an eight-hour lifetime.
- Added PDF report generation.
- Added multilingual support (French, English and German).
- Added support for smartphones and tablets.
- Restored the latest calculation automatically when returning from the **Help** or **About** pages.

### Changed

- Centralized HTML templates using `base.html`.
- Reorganized the business logic into the `services` package.
- Centralized application version management.
- Improved validation of Time of Day values.
- Improved calculation robustness.
- Optimized Flask session management.

### Documentation

- Added deployment prerequisites.
- Added deployment and administration guides.
- Added a security checklist.
- Added the project `README.md`.

### Validation

- Validated operation under Windows.
- Validated operation under Ubuntu Linux.
- Validated operation on Android smartphones.
- Validated PDF generation in all supported languages.
- Validated deployment with Gunicorn and systemd.
- Prepared the application for deployment within the French Ski Federation infrastructure.

---

## [1.00] - 2026-05

### Added

- First operational release of **EET Calculator**.
- Implemented Equivalent Electronic Time (EET) calculation according to FIS rules.
- Added timing reference management.
- Added automatic correction calculation.
- Added delta display.
- Added configurable TM and TE precision.
- Added PDF report generation.
- Added multilingual support (French, English and German).
- Added **Help** and **About** pages.

### Architecture

- Initial Flask application architecture.
- Introduced HTML templates, CSS stylesheets and JavaScript validation.
- Separated calculation services from the user interface.

---

Earlier development versions were internal and are not documented in this changelog.