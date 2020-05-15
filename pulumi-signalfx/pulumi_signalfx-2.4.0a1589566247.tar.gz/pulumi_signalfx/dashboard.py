# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Dashboard(pulumi.CustomResource):
    authorized_writer_teams: pulumi.Output[list]
    """
    Team IDs that have write access to this dashboard
    """
    authorized_writer_users: pulumi.Output[list]
    """
    User IDs that have write access to this dashboard
    """
    charts: pulumi.Output[list]
    """
    Chart ID and layout information for the charts in the dashboard.

      * `chartId` (`str`) - ID of the chart to display.
      * `column` (`float`) - Column number for the layout.
      * `height` (`float`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
      * `row` (`float`) - The row to show the chart in (zero-based); if `height > 1`, this value represents the topmost row of the chart (greater than or equal to `0`).
      * `width` (`float`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.
    """
    charts_resolution: pulumi.Output[str]
    """
    Specifies the chart data display resolution for charts in this dashboard. Value can be one of `"default"`,  `"low"`, `"high"`, or  `"highest"`.
    """
    columns: pulumi.Output[list]
    """
    Column number for the layout.

      * `chartIds` (`list`) - List of IDs of the charts to display.
      * `column` (`float`) - Column number for the layout.
      * `height` (`float`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
      * `width` (`float`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.
    """
    dashboard_group: pulumi.Output[str]
    """
    The ID of the dashboard group that contains the dashboard.
    """
    description: pulumi.Output[str]
    """
    Variable description.
    """
    discovery_options_query: pulumi.Output[str]
    discovery_options_selectors: pulumi.Output[list]
    end_time: pulumi.Output[float]
    """
    Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
    """
    event_overlays: pulumi.Output[list]
    """
    Specify a list of event overlays to include in the dashboard. Note: These overlays correspond to the *suggested* event overlays specified in the web UI, and they're not automatically applied as active overlays. To set default active event overlays, use the `selected_event_overlay` property instead.

      * `color` (`str`) - Color to use : gray, blue, azure, navy, brown, orange, yellow, iris, magenta, pink, purple, violet, lilac, emerald, green, aquamarine.
      * `label` (`str`) - Text shown in the dropdown when selecting this overlay from the menu.
      * `line` (`bool`) - Show a vertical line for the event. `false` by default.
      * `signal` (`str`) - Search term used to choose the events shown in the overlay.
      * `sources` (`list`) - Each element specifies a filter to use against the signal specified in the `signal`.
        * `negated` (`bool`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
        * `property` (`str`) - The name of a dimension to filter against.
        * `values` (`list`) - A list of values to be used with the `property`, they will be combined via `OR`.

      * `type` (`str`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.
    """
    filters: pulumi.Output[list]
    """
    Filter to apply to the charts when displaying the dashboard.

      * `applyIfExist` (`bool`) - If true, this variable will also match data that doesn't have this property at all.
      * `negated` (`bool`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
      * `property` (`str`) - The name of a dimension to filter against.
      * `values` (`list`) - A list of values to be used with the `property`, they will be combined via `OR`.
    """
    grids: pulumi.Output[list]
    """
    Grid dashboard layout. Charts listed will be placed in a grid by row with the same width and height. If a chart cannot fit in a row, it will be placed automatically in the next row.

      * `chartIds` (`list`) - List of IDs of the charts to display.
      * `height` (`float`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
      * `width` (`float`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.
    """
    name: pulumi.Output[str]
    """
    Name of the dashboard.
    """
    selected_event_overlays: pulumi.Output[list]
    """
    Defines event overlays which are enabled by **default**. Any overlay specified here should have an accompanying entry in `event_overlay`, which are similar to the properties here.

      * `signal` (`str`) - Search term used to choose the events shown in the overlay.
      * `sources` (`list`) - Each element specifies a filter to use against the signal specified in the `signal`.
        * `negated` (`bool`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
        * `property` (`str`) - The name of a dimension to filter against.
        * `values` (`list`) - A list of values to be used with the `property`, they will be combined via `OR`.

      * `type` (`str`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.
    """
    start_time: pulumi.Output[float]
    """
    Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
    """
    time_range: pulumi.Output[str]
    """
    The time range prior to now to visualize. SignalFx time syntax (e.g. `"-5m"`, `"-1h"`).
    """
    url: pulumi.Output[str]
    """
    URL of the dashboard
    """
    variables: pulumi.Output[list]
    """
    Dashboard variable to apply to each chart in the dashboard.

      * `alias` (`str`) - An alias for the dashboard variable. This text will appear as the label for the dropdown field on the dashboard.
      * `applyIfExist` (`bool`) - If true, this variable will also match data that doesn't have this property at all.
      * `description` (`str`) - Variable description.
      * `property` (`str`) - The name of a dimension to filter against.
      * `replaceOnly` (`bool`) - If `true`, this variable will only apply to charts that have a filter for the property.
      * `restrictedSuggestions` (`bool`) - If `true`, this variable may only be set to the values listed in `values_suggested` and only these values will appear in autosuggestion menus. `false` by default.
      * `valueRequired` (`bool`) - Determines whether a value is required for this variable (and therefore whether it will be possible to view this dashboard without this filter applied). `false` by default.
      * `values` (`list`) - A list of values to be used with the `property`, they will be combined via `OR`.
      * `valuesSuggesteds` (`list`) - A list of strings of suggested values for this variable; these suggestions will receive priority when values are autosuggested for this variable.
    """
    def __init__(__self__, resource_name, opts=None, authorized_writer_teams=None, authorized_writer_users=None, charts=None, charts_resolution=None, columns=None, dashboard_group=None, description=None, discovery_options_query=None, discovery_options_selectors=None, end_time=None, event_overlays=None, filters=None, grids=None, name=None, selected_event_overlays=None, start_time=None, time_range=None, variables=None, __props__=None, __name__=None, __opts__=None):
        """
        A dashboard is a curated collection of specific charts and supports dimensional [filters](http://docs.signalfx.com/en/latest/dashboards/dashboard-filter-dynamic.html#filter-dashboard-charts), [dashboard variables](http://docs.signalfx.com/en/latest/dashboards/dashboard-filter-dynamic.html#dashboard-variables) and [time range](http://docs.signalfx.com/en/latest/_sidebars-and-includes/using-time-range-selector.html#time-range-selector) options. These options are applied to all charts in the dashboard, providing a consistent view of the data displayed in that dashboard. This also means that when you open a chart to drill down for more details, you are viewing the same data that is visible in the dashboard view.

        > **NOTE** Since every dashboard is included in a `dashboard group` (SignalFx collection of dashboards), you need to create that first and reference it as shown in the example.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_signalfx as signalfx

        mydashboard0 = signalfx.Dashboard("mydashboard0",
            dashboard_group=signalfx_dashboard_group["mydashboardgroup0"]["id"],
            time_range="-30m",
            filter=[{
                "property": "collector",
                "values": [
                    "cpu",
                    "Diamond",
                ],
            }],
            variable=[{
                "property": "region",
                "alias": "region",
                "values": ["uswest-1-"],
            }],
            chart=[
                {
                    "chartId": signalfx_time_chart["mychart0"]["id"],
                    "width": 12,
                    "height": 1,
                },
                {
                    "chartId": signalfx_time_chart["mychart1"]["id"],
                    "width": 5,
                    "height": 2,
                },
            ])
        ```

        ### Column

        ```python
        import pulumi
        import pulumi_signalfx as signalfx

        load = signalfx.Dashboard("load",
            columns=[
                {
                    "chartIds": [[__item["id"] for __item in signalfx_single_value_chart["rps"]]],
                    "width": 2,
                },
                {
                    "chartIds": [[__item["id"] for __item in signalfx_time_chart["cpu_capacity"]]],
                    "column": 2,
                    "width": 4,
                },
            ],
            dashboard_group=signalfx_dashboard_group["example"]["id"])
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] authorized_writer_teams: Team IDs that have write access to this dashboard
        :param pulumi.Input[list] authorized_writer_users: User IDs that have write access to this dashboard
        :param pulumi.Input[list] charts: Chart ID and layout information for the charts in the dashboard.
        :param pulumi.Input[str] charts_resolution: Specifies the chart data display resolution for charts in this dashboard. Value can be one of `"default"`,  `"low"`, `"high"`, or  `"highest"`.
        :param pulumi.Input[list] columns: Column number for the layout.
        :param pulumi.Input[str] dashboard_group: The ID of the dashboard group that contains the dashboard.
        :param pulumi.Input[str] description: Variable description.
        :param pulumi.Input[float] end_time: Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
        :param pulumi.Input[list] event_overlays: Specify a list of event overlays to include in the dashboard. Note: These overlays correspond to the *suggested* event overlays specified in the web UI, and they're not automatically applied as active overlays. To set default active event overlays, use the `selected_event_overlay` property instead.
        :param pulumi.Input[list] filters: Filter to apply to the charts when displaying the dashboard.
        :param pulumi.Input[list] grids: Grid dashboard layout. Charts listed will be placed in a grid by row with the same width and height. If a chart cannot fit in a row, it will be placed automatically in the next row.
        :param pulumi.Input[str] name: Name of the dashboard.
        :param pulumi.Input[list] selected_event_overlays: Defines event overlays which are enabled by **default**. Any overlay specified here should have an accompanying entry in `event_overlay`, which are similar to the properties here.
        :param pulumi.Input[float] start_time: Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
        :param pulumi.Input[str] time_range: The time range prior to now to visualize. SignalFx time syntax (e.g. `"-5m"`, `"-1h"`).
        :param pulumi.Input[list] variables: Dashboard variable to apply to each chart in the dashboard.

        The **charts** object supports the following:

          * `chartId` (`pulumi.Input[str]`) - ID of the chart to display.
          * `column` (`pulumi.Input[float]`) - Column number for the layout.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `row` (`pulumi.Input[float]`) - The row to show the chart in (zero-based); if `height > 1`, this value represents the topmost row of the chart (greater than or equal to `0`).
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **columns** object supports the following:

          * `chartIds` (`pulumi.Input[list]`) - List of IDs of the charts to display.
          * `column` (`pulumi.Input[float]`) - Column number for the layout.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **event_overlays** object supports the following:

          * `color` (`pulumi.Input[str]`) - Color to use : gray, blue, azure, navy, brown, orange, yellow, iris, magenta, pink, purple, violet, lilac, emerald, green, aquamarine.
          * `label` (`pulumi.Input[str]`) - Text shown in the dropdown when selecting this overlay from the menu.
          * `line` (`pulumi.Input[bool]`) - Show a vertical line for the event. `false` by default.
          * `signal` (`pulumi.Input[str]`) - Search term used to choose the events shown in the overlay.
          * `sources` (`pulumi.Input[list]`) - Each element specifies a filter to use against the signal specified in the `signal`.
            * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
            * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
            * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

          * `type` (`pulumi.Input[str]`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.

        The **filters** object supports the following:

          * `applyIfExist` (`pulumi.Input[bool]`) - If true, this variable will also match data that doesn't have this property at all.
          * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
          * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
          * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

        The **grids** object supports the following:

          * `chartIds` (`pulumi.Input[list]`) - List of IDs of the charts to display.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **selected_event_overlays** object supports the following:

          * `signal` (`pulumi.Input[str]`) - Search term used to choose the events shown in the overlay.
          * `sources` (`pulumi.Input[list]`) - Each element specifies a filter to use against the signal specified in the `signal`.
            * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
            * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
            * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

          * `type` (`pulumi.Input[str]`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.

        The **variables** object supports the following:

          * `alias` (`pulumi.Input[str]`) - An alias for the dashboard variable. This text will appear as the label for the dropdown field on the dashboard.
          * `applyIfExist` (`pulumi.Input[bool]`) - If true, this variable will also match data that doesn't have this property at all.
          * `description` (`pulumi.Input[str]`) - Variable description.
          * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
          * `replaceOnly` (`pulumi.Input[bool]`) - If `true`, this variable will only apply to charts that have a filter for the property.
          * `restrictedSuggestions` (`pulumi.Input[bool]`) - If `true`, this variable may only be set to the values listed in `values_suggested` and only these values will appear in autosuggestion menus. `false` by default.
          * `valueRequired` (`pulumi.Input[bool]`) - Determines whether a value is required for this variable (and therefore whether it will be possible to view this dashboard without this filter applied). `false` by default.
          * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.
          * `valuesSuggesteds` (`pulumi.Input[list]`) - A list of strings of suggested values for this variable; these suggestions will receive priority when values are autosuggested for this variable.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['authorized_writer_teams'] = authorized_writer_teams
            __props__['authorized_writer_users'] = authorized_writer_users
            __props__['charts'] = charts
            __props__['charts_resolution'] = charts_resolution
            __props__['columns'] = columns
            if dashboard_group is None:
                raise TypeError("Missing required property 'dashboard_group'")
            __props__['dashboard_group'] = dashboard_group
            __props__['description'] = description
            __props__['discovery_options_query'] = discovery_options_query
            __props__['discovery_options_selectors'] = discovery_options_selectors
            __props__['end_time'] = end_time
            __props__['event_overlays'] = event_overlays
            __props__['filters'] = filters
            __props__['grids'] = grids
            __props__['name'] = name
            __props__['selected_event_overlays'] = selected_event_overlays
            __props__['start_time'] = start_time
            __props__['time_range'] = time_range
            __props__['variables'] = variables
            __props__['url'] = None
        super(Dashboard, __self__).__init__(
            'signalfx:index/dashboard:Dashboard',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, authorized_writer_teams=None, authorized_writer_users=None, charts=None, charts_resolution=None, columns=None, dashboard_group=None, description=None, discovery_options_query=None, discovery_options_selectors=None, end_time=None, event_overlays=None, filters=None, grids=None, name=None, selected_event_overlays=None, start_time=None, time_range=None, url=None, variables=None):
        """
        Get an existing Dashboard resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] authorized_writer_teams: Team IDs that have write access to this dashboard
        :param pulumi.Input[list] authorized_writer_users: User IDs that have write access to this dashboard
        :param pulumi.Input[list] charts: Chart ID and layout information for the charts in the dashboard.
        :param pulumi.Input[str] charts_resolution: Specifies the chart data display resolution for charts in this dashboard. Value can be one of `"default"`,  `"low"`, `"high"`, or  `"highest"`.
        :param pulumi.Input[list] columns: Column number for the layout.
        :param pulumi.Input[str] dashboard_group: The ID of the dashboard group that contains the dashboard.
        :param pulumi.Input[str] description: Variable description.
        :param pulumi.Input[float] end_time: Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
        :param pulumi.Input[list] event_overlays: Specify a list of event overlays to include in the dashboard. Note: These overlays correspond to the *suggested* event overlays specified in the web UI, and they're not automatically applied as active overlays. To set default active event overlays, use the `selected_event_overlay` property instead.
        :param pulumi.Input[list] filters: Filter to apply to the charts when displaying the dashboard.
        :param pulumi.Input[list] grids: Grid dashboard layout. Charts listed will be placed in a grid by row with the same width and height. If a chart cannot fit in a row, it will be placed automatically in the next row.
        :param pulumi.Input[str] name: Name of the dashboard.
        :param pulumi.Input[list] selected_event_overlays: Defines event overlays which are enabled by **default**. Any overlay specified here should have an accompanying entry in `event_overlay`, which are similar to the properties here.
        :param pulumi.Input[float] start_time: Seconds since epoch. Used for visualization. You must specify time_span_type = `"absolute"` too.
        :param pulumi.Input[str] time_range: The time range prior to now to visualize. SignalFx time syntax (e.g. `"-5m"`, `"-1h"`).
        :param pulumi.Input[str] url: URL of the dashboard
        :param pulumi.Input[list] variables: Dashboard variable to apply to each chart in the dashboard.

        The **charts** object supports the following:

          * `chartId` (`pulumi.Input[str]`) - ID of the chart to display.
          * `column` (`pulumi.Input[float]`) - Column number for the layout.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `row` (`pulumi.Input[float]`) - The row to show the chart in (zero-based); if `height > 1`, this value represents the topmost row of the chart (greater than or equal to `0`).
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **columns** object supports the following:

          * `chartIds` (`pulumi.Input[list]`) - List of IDs of the charts to display.
          * `column` (`pulumi.Input[float]`) - Column number for the layout.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **event_overlays** object supports the following:

          * `color` (`pulumi.Input[str]`) - Color to use : gray, blue, azure, navy, brown, orange, yellow, iris, magenta, pink, purple, violet, lilac, emerald, green, aquamarine.
          * `label` (`pulumi.Input[str]`) - Text shown in the dropdown when selecting this overlay from the menu.
          * `line` (`pulumi.Input[bool]`) - Show a vertical line for the event. `false` by default.
          * `signal` (`pulumi.Input[str]`) - Search term used to choose the events shown in the overlay.
          * `sources` (`pulumi.Input[list]`) - Each element specifies a filter to use against the signal specified in the `signal`.
            * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
            * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
            * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

          * `type` (`pulumi.Input[str]`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.

        The **filters** object supports the following:

          * `applyIfExist` (`pulumi.Input[bool]`) - If true, this variable will also match data that doesn't have this property at all.
          * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
          * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
          * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

        The **grids** object supports the following:

          * `chartIds` (`pulumi.Input[list]`) - List of IDs of the charts to display.
          * `height` (`pulumi.Input[float]`) - How many rows every chart should take up (greater than or equal to 1). 1 by default.
          * `width` (`pulumi.Input[float]`) - How many columns (out of a total of `12`) every chart should take up (between `1` and `12`). `12` by default.

        The **selected_event_overlays** object supports the following:

          * `signal` (`pulumi.Input[str]`) - Search term used to choose the events shown in the overlay.
          * `sources` (`pulumi.Input[list]`) - Each element specifies a filter to use against the signal specified in the `signal`.
            * `negated` (`pulumi.Input[bool]`) - If true,  only data that does not match the specified value of the specified property appear in the event overlay. Defaults to `false`.
            * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
            * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.

          * `type` (`pulumi.Input[str]`) - Can be set to `eventTimeSeries` (the default) to refer to externally reported events, or `detectorEvents` to refer to events from detector triggers.

        The **variables** object supports the following:

          * `alias` (`pulumi.Input[str]`) - An alias for the dashboard variable. This text will appear as the label for the dropdown field on the dashboard.
          * `applyIfExist` (`pulumi.Input[bool]`) - If true, this variable will also match data that doesn't have this property at all.
          * `description` (`pulumi.Input[str]`) - Variable description.
          * `property` (`pulumi.Input[str]`) - The name of a dimension to filter against.
          * `replaceOnly` (`pulumi.Input[bool]`) - If `true`, this variable will only apply to charts that have a filter for the property.
          * `restrictedSuggestions` (`pulumi.Input[bool]`) - If `true`, this variable may only be set to the values listed in `values_suggested` and only these values will appear in autosuggestion menus. `false` by default.
          * `valueRequired` (`pulumi.Input[bool]`) - Determines whether a value is required for this variable (and therefore whether it will be possible to view this dashboard without this filter applied). `false` by default.
          * `values` (`pulumi.Input[list]`) - A list of values to be used with the `property`, they will be combined via `OR`.
          * `valuesSuggesteds` (`pulumi.Input[list]`) - A list of strings of suggested values for this variable; these suggestions will receive priority when values are autosuggested for this variable.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["authorized_writer_teams"] = authorized_writer_teams
        __props__["authorized_writer_users"] = authorized_writer_users
        __props__["charts"] = charts
        __props__["charts_resolution"] = charts_resolution
        __props__["columns"] = columns
        __props__["dashboard_group"] = dashboard_group
        __props__["description"] = description
        __props__["discovery_options_query"] = discovery_options_query
        __props__["discovery_options_selectors"] = discovery_options_selectors
        __props__["end_time"] = end_time
        __props__["event_overlays"] = event_overlays
        __props__["filters"] = filters
        __props__["grids"] = grids
        __props__["name"] = name
        __props__["selected_event_overlays"] = selected_event_overlays
        __props__["start_time"] = start_time
        __props__["time_range"] = time_range
        __props__["url"] = url
        __props__["variables"] = variables
        return Dashboard(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

