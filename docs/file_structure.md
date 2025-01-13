# File structure
<!-- prettier-ignore-start -->
<!-- Don't forget the two tabs! -->
    .
    ├── README.rst                                        <- The project overview.
    ├── CODE_OF_CONDUCT.rst                               <- The project's code of conduct.
    ├── CONTRIBUTING.rst                                  <- The project's contribution guidelines.
    ├── LICENSE.rst                                       <- The project's licensing data.
    ├── PROJECT_GOVERNANCE.rst                            <- The project's governance information.
    ├── SECURITY.rst                                      <- The project's security and version support information.
    ├── docs                                              <- All project documents.
    │   ├── developers                                    <- All documentation aimed at developers.
    │   ├── users                                         <- All documentation aimed at users.
    ├── sphinx-docs                                       <- The project's Sphinx documentation.
    └── src                                               <- The source code for the project.
        ├── source_templates                              <- A template structure for creating your own source.
        │   └── weather_provider_sources                  <- The base source package used for accessing weather data providers.
        │       └── example_source                        <- An example source package with dummy models.
        └── weather_provider_libraries                    <- The libraries package for accessing weather data providers.
            ├── base_classes                              <- The base interaction classes for the library
            │   ├── controller.py
            │   ├── model.py
            │   ├── source.py
            │   ├── storage.py
            │   └── update_manager.py
            ├── schemas                                   <- The schemas used to validate and format data factors.
            │   ├── eccodes_schema.json
            │   └── harmonization_schema.json
            └── utils                                     <- The utility functions used by the library.
                ├── coordinate_utils.py
                ├── timeperiod_utils.py
                ├── xarray_formatting_utils.py
                └── zarr_utils.py

<!-- prettier-ignore-end -->
