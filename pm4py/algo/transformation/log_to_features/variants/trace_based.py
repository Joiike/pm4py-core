'''
    This file is part of PM4Py (More Info: https://pm4py.fit.fraunhofer.de).

    PM4Py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PM4Py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PM4Py.  If not, see <https://www.gnu.org/licenses/>.
'''
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Union, Tuple

import pandas as pd

from pm4py.objects.conversion.log import converter
from pm4py.objects.log.obj import EventLog, Trace, Event
from pm4py.objects.log.util import dataframe_utils
from pm4py.util import constants
from pm4py.util import exec_utils
from pm4py.util import xes_constants as xes


class Parameters(Enum):
    ENABLE_ACTIVITY_DEF_REPRESENTATION = "enable_activity_def_representation"
    ENABLE_SUCC_DEF_REPRESENTATION = "enable_succ_def_representation"
    STR_TRACE_ATTRIBUTES = "str_tr_attr"
    STR_EVENT_ATTRIBUTES = "str_ev_attr"
    NUM_TRACE_ATTRIBUTES = "num_tr_attr"
    NUM_EVENT_ATTRIBUTES = "num_ev_attr"
    STR_EVSUCC_ATTRIBUTES = "str_evsucc_attr"
    FEATURE_NAMES = "feature_names"


def get_string_trace_attribute_rep(trace: Trace, trace_attribute: str) -> str:
    """
    Get a representation of the feature name associated to a string trace attribute value

    Parameters
    ------------
    trace
        Trace of the log
    trace_attribute
        Attribute of the trace to consider

    Returns
    ------------
    rep
        Representation of the feature name associated to a string trace attribute value
    """
    if trace_attribute in trace.attributes:
        return "trace:" + str(trace_attribute) + "@" + str(trace.attributes[trace_attribute])
    return "trace:" + str(trace_attribute) + "@UNDEFINED"


def get_all_string_trace_attribute_values(log: EventLog, trace_attribute: str) -> List[str]:
    """
    Get all string trace attribute values representations for a log

    Parameters
    ------------
    log
        Trace log
    trace_attribute
        Attribute of the trace to consider

    Returns
    ------------
    list
        List containing for each trace a representation of the feature name associated to the attribute
    """
    values = set()
    for trace in log:
        values.add(get_string_trace_attribute_rep(trace, trace_attribute))
    return list(sorted(values))


def get_string_event_attribute_rep(event: Event, event_attribute: str) -> str:
    """
    Get a representation of the feature name associated to a string event attribute value

    Parameters
    ------------
    event
        Single event of a trace
    event_attribute
        Event attribute to consider

    Returns
    ------------
    rep
        Representation of the feature name associated to a string event attribute value
    """
    return "event:" + str(event_attribute) + "@" + str(event[event_attribute])


def get_values_event_attribute_for_trace(trace: Trace, event_attribute: str) -> Set[str]:
    """
    Get all the representations for the events of a trace associated to a string event attribute values

    Parameters
    -------------
    trace
        Trace of the log
    event_attribute
        Event attribute to consider

    Returns
    -------------
    values
        All feature names present for the given attribute in the given trace
    """
    values_trace = set()
    for event in trace:
        if event_attribute in event:
            values_trace.add(get_string_event_attribute_rep(event, event_attribute))
    if not values_trace:
        values_trace.add("event:" + str(event_attribute) + "@UNDEFINED")
    return values_trace


def get_all_string_event_attribute_values(log: EventLog, event_attribute: str) -> List[str]:
    """
    Get all the representations for all the traces of the log associated to a string event attribute values

    Parameters
    ------------
    log
        Trace of the log
    event_attribute
        Event attribute to consider

    Returns
    ------------
    values
        All feature names present for the given attribute in the given log
    """
    values = set()
    for trace in log:
        values = values.union(get_values_event_attribute_for_trace(trace, event_attribute))
    return list(sorted(values))


def get_string_event_attribute_succession_rep(event1: Event, event2: Event, event_attribute: str) -> str:
    """
    Get a representation of the feature name associated to a string event attribute value

    Parameters
    ------------
    event1
        First event of the succession
    event2
        Second event of the succession
    event_attribute
        Event attribute to consider

    Returns
    ------------
    rep
        Representation of the feature name associated to a string event attribute value
    """
    return "succession:" + str(event_attribute) + "@" + str(event1[event_attribute]) + "#" + str(
        event2[event_attribute])


def get_values_event_attribute_succession_for_trace(trace: Trace, event_attribute: str) -> Set[str]:
    """
    Get all the representations for the events of a trace associated to a string event attribute succession values

    Parameters
    -------------
    trace
        Trace of the log
    event_attribute
        Event attribute to consider

    Returns
    -------------
    values
        All feature names present for the given attribute succession in the given trace
    """
    values_trace = set()
    for i in range(len(trace) - 1):
        event1 = trace[i]
        event2 = trace[i + 1]
        if event_attribute in event1 and event_attribute in event2:
            values_trace.add(get_string_event_attribute_succession_rep(event1, event2, event_attribute))
    if not values_trace:
        values_trace.add("succession:" + str(event_attribute) + "@UNDEFINED")
    return values_trace


def get_all_string_event_succession_attribute_values(log: EventLog, event_attribute: str) -> List[str]:
    """
    Get all the representations for all the traces of the log associated to a string event attribute succession values

    Parameters
    ------------
    log
        Trace of the log
    event_attribute
        Event attribute to consider

    Returns
    ------------
    values
        All feature names present for the given attribute succession in the given log
    """
    values = set()
    for trace in log:
        values = values.union(get_values_event_attribute_succession_for_trace(trace, event_attribute))
    return list(sorted(values))


def get_numeric_trace_attribute_rep(trace_attribute: str) -> str:
    """
    Get the feature name associated to a numeric trace attribute

    Parameters
    ------------
    trace_attribute
        Name of the trace attribute

    Returns
    ------------
    feature_name
        Name of the feature
    """
    return "trace:" + trace_attribute


def get_numeric_trace_attribute_value(trace: Trace, trace_attribute: str) -> Union[int, float]:
    """
    Get the value of a numeric trace attribute from a given trace

    Parameters
    ------------
    trace
        Trace of the log

    Returns
    ------------
    value
        Value of the numeric trace attribute for the given trace
    """
    if trace_attribute in trace.attributes:
        return trace.attributes[trace_attribute]
    raise Exception("at least a trace without trace attribute: " + trace_attribute)


def get_numeric_event_attribute_rep(event_attribute: str) -> str:
    """
    Get the feature name associated to a numeric event attribute

    Parameters
    ------------
    event_attribute
        Name of the event attribute

    Returns
    -------------
    feature_name
        Name of the feature
    """
    return "event:" + event_attribute


def get_numeric_event_attribute_value(event: Event, event_attribute: str) -> Union[int, float]:
    """
    Get the value of a numeric event attribute from a given event

    Parameters
    -------------
    event
        Event

    Returns
    -------------
    value
        Value of the numeric event attribute for the given event
    """
    if event_attribute in event:
        return event[event_attribute]
    return None


def get_numeric_event_attribute_value_trace(trace: Trace, event_attribute: str) -> Union[int, float]:
    """
    Get the value of the last occurrence of a numeric event attribute given a trace

    Parameters
    -------------
    trace
        Trace of the log

    Returns
    -------------
    value
        Value of the last occurrence of a numeric trace attribute for the given trace
    """
    non_zero_values = []
    for event in trace:
        value = get_numeric_event_attribute_value(event, event_attribute)
        if value is not None:
            non_zero_values.append(value)
    if len(non_zero_values) > 0:
        return non_zero_values[-1]
    raise Exception("at least a trace without any event with event attribute: " + event_attribute)


def get_default_representation_with_attribute_names(log: EventLog, parameters: Optional[Dict[Union[str, Parameters], Any]] = None,
                                                    feature_names: Optional[List[str]] = None) -> Tuple[
    Any, List[str], List[str], List[str], List[str], List[str]]:
    """
    Gets the default data representation of an event log (for process tree building)
    returning also the attribute names

    Parameters
    -------------
    log
        Trace log
    parameters
        Possible parameters of the algorithm
    feature_names
        (If provided) Feature to use in the representation of the log

    Returns
    -------------
    data
        Data to provide for decision tree learning
    feature_names
        Names of the features, in order
    """
    from pm4py.statistics.attributes.log.select import select_attributes_from_log_for_tree

    if parameters is None:
        parameters = {}

    enable_activity_def_representation = exec_utils.get_param_value(Parameters.ENABLE_ACTIVITY_DEF_REPRESENTATION,
                                                                    parameters, False)
    enable_succ_def_representation = exec_utils.get_param_value(Parameters.ENABLE_SUCC_DEF_REPRESENTATION, parameters,
                                                                False)

    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    blacklist = parameters["blacklist"] if "blacklist" in parameters else []

    str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr = select_attributes_from_log_for_tree(log)
    str_evsucc_attr = None

    if enable_succ_def_representation:
        str_evsucc_attr = [activity_key]
    if enable_activity_def_representation and activity_key not in str_ev_attr:
        str_ev_attr.append(activity_key)

    str_tr_attr = [x for x in str_tr_attr if x not in blacklist]
    str_ev_attr = [x for x in str_ev_attr if x not in blacklist]
    num_tr_attr = [x for x in num_tr_attr if x not in blacklist]
    num_ev_attr = [x for x in num_ev_attr if x not in blacklist]
    if str_evsucc_attr is not None:
        str_evsucc_attr = [x for x in str_evsucc_attr if x not in blacklist]

    data, feature_names = get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr,
                                             str_evsucc_attr=str_evsucc_attr,
                                             feature_names=feature_names)

    return data, feature_names, str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr


def get_default_representation(log: EventLog, parameters: Optional[Dict[Union[str, Parameters], Any]] = None,
                               feature_names: Optional[List[str]] = None) -> Tuple[Any, List[str]]:
    """
    Gets the default data representation of an event log (for process tree building)

    Parameters
    -------------
    log
        Trace log
    parameters
        Possible parameters of the algorithm
    feature_names
        (If provided) Feature to use in the representation of the log

    Returns
    -------------
    data
        Data to provide for decision tree learning
    feature_names
        Names of the features, in order
    """
    from pm4py.statistics.attributes.log.select import select_attributes_from_log_for_tree

    if parameters is None:
        parameters = {}

    enable_activity_def_representation = exec_utils.get_param_value(Parameters.ENABLE_ACTIVITY_DEF_REPRESENTATION,
                                                                    parameters, True)
    enable_succ_def_representation = exec_utils.get_param_value(Parameters.ENABLE_SUCC_DEF_REPRESENTATION, parameters,
                                                                True)

    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    blacklist = parameters["blacklist"] if "blacklist" in parameters else []

    str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr = select_attributes_from_log_for_tree(log)
    str_evsucc_attr = None

    if enable_succ_def_representation:
        str_evsucc_attr = [activity_key]
    if enable_activity_def_representation and activity_key not in str_ev_attr:
        str_ev_attr.append(activity_key)

    str_tr_attr = [x for x in str_tr_attr if x not in blacklist]
    str_ev_attr = [x for x in str_ev_attr if x not in blacklist]
    num_tr_attr = [x for x in num_tr_attr if x not in blacklist]
    num_ev_attr = [x for x in num_ev_attr if x not in blacklist]
    if str_evsucc_attr is not None:
        str_evsucc_attr = [x for x in str_evsucc_attr if x not in blacklist]

    return get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr, str_evsucc_attr=str_evsucc_attr,
                              feature_names=feature_names)


def get_representation(log: EventLog, str_tr_attr: List[str], str_ev_attr: List[str], num_tr_attr: List[str],
                       num_ev_attr: List[str], str_evsucc_attr: Optional[List[str]] = None,
                       feature_names: Optional[List[str]] = None) -> Tuple[Any, List[str]]:
    """
    Get a representation of the event log that is suited for the data part of the decision tree learning

    NOTE: this function only encodes the last value seen for each attribute

    Parameters
    -------------
    log
        Trace log
    str_tr_attr
        List of string trace attributes to consider in data vector creation
    str_ev_attr
        List of string event attributes to consider in data vector creation
    num_tr_attr
        List of numeric trace attributes to consider in data vector creation
    num_ev_attr
        List of numeric event attributes to consider in data vector creation
    str_evsucc_attr
        List of attributes succession of values to consider in data vector creation
    feature_names
        (If provided) Feature to use in the representation of the log

    Returns
    -------------
    data
        Data to provide for decision tree learning
    feature_names
        Names of the features, in order
    """
    data = []
    dictionary = {}
    count = 0
    if feature_names is None:
        feature_names = []
        for trace_attribute in str_tr_attr:
            values = get_all_string_trace_attribute_values(log, trace_attribute)
            for value in values:
                dictionary[value] = count
                feature_names.append(value)
                count = count + 1
        for event_attribute in str_ev_attr:
            values = get_all_string_event_attribute_values(log, event_attribute)
            for value in values:
                dictionary[value] = count
                feature_names.append(value)
                count = count + 1
        for trace_attribute in num_tr_attr:
            dictionary[get_numeric_trace_attribute_rep(trace_attribute)] = count
            feature_names.append(get_numeric_trace_attribute_rep(trace_attribute))
            count = count + 1
        for event_attribute in num_ev_attr:
            dictionary[get_numeric_event_attribute_rep(event_attribute)] = count
            feature_names.append(get_numeric_event_attribute_rep(event_attribute))
            count = count + 1
        if str_evsucc_attr:
            for event_attribute in str_evsucc_attr:
                values = get_all_string_event_succession_attribute_values(log, event_attribute)
                for value in values:
                    dictionary[value] = count
                    feature_names.append(value)
                    count = count + 1
    else:
        count = len(feature_names)
        for index, value in enumerate(feature_names):
            dictionary[value] = index
    for trace in log:
        trace_rep = [0] * count
        for trace_attribute in str_tr_attr:
            trace_attr_rep = get_string_trace_attribute_rep(trace, trace_attribute)
            if trace_attr_rep in dictionary:
                trace_rep[dictionary[trace_attr_rep]] = 1
        for event_attribute in str_ev_attr:
            values = get_values_event_attribute_for_trace(trace, event_attribute)
            for value in values:
                if value in dictionary:
                    trace_rep[dictionary[value]] = 1
        for trace_attribute in num_tr_attr:
            this_value = get_numeric_trace_attribute_rep(trace_attribute)
            if this_value in dictionary:
                trace_rep[dictionary[this_value]] = get_numeric_trace_attribute_value(
                    trace, trace_attribute)
        for event_attribute in num_ev_attr:
            this_value = get_numeric_event_attribute_rep(event_attribute)
            if this_value in dictionary:
                trace_rep[dictionary[this_value]] = get_numeric_event_attribute_value_trace(
                    trace, event_attribute)
        if str_evsucc_attr:
            for event_attribute in str_evsucc_attr:
                values = get_values_event_attribute_succession_for_trace(trace, event_attribute)
                for value in values:
                    if value in dictionary:
                        trace_rep[dictionary[value]] = 1
        data.append(trace_rep)
    # data = np.asarray(data)
    return data, feature_names


def apply(log: EventLog, parameters: Optional[Dict[Union[str, Parameters], Any]] = None) -> Tuple[Any, List[str]]:
    """
    Extract the features from an event log (a vector for each trace)

    Parameters
    -----------------
    log
        Log
    parameters
        Parameters of the algorithm, including:
        - STR_TRACE_ATTRIBUTES => string trace attributes to consider in the features extraction
        - STR_EVENT_ATTRIBUTES => string event attributes to consider in the features extraction
        - NUM_TRACE_ATTRIBUTES => numeric trace attributes to consider in the features extraction
        - NUM_EVENT_ATTRIBUTES => numeric event attributes to consider in the features extraction
        - STR_EVSUCC_ATTRIBUTES => succession of event attributes to consider in the features extraction
        - FEATURE_NAMES => features to consider (in the given order)

    Returns
    -------------
    data
        Data to provide for decision tree learning
    feature_names
        Names of the features, in order
    """
    if parameters is None:
        parameters = {}

    str_tr_attr = exec_utils.get_param_value(Parameters.STR_TRACE_ATTRIBUTES, parameters, None)
    num_tr_attr = exec_utils.get_param_value(Parameters.NUM_TRACE_ATTRIBUTES, parameters, None)
    str_ev_attr = exec_utils.get_param_value(Parameters.STR_EVENT_ATTRIBUTES, parameters, None)
    num_ev_attr = exec_utils.get_param_value(Parameters.NUM_EVENT_ATTRIBUTES, parameters, None)
    str_evsucc_attr = exec_utils.get_param_value(Parameters.STR_EVSUCC_ATTRIBUTES, parameters, None)
    feature_names = exec_utils.get_param_value(Parameters.FEATURE_NAMES, parameters, None)

    if str_tr_attr is None:
        str_tr_attr = []

    if num_tr_attr is None:
        num_tr_attr = []

    if str_ev_attr is None:
        str_ev_attr = []

    if num_ev_attr is None:
        num_ev_attr = []

    if type(log) is pd.DataFrame:
        if str_tr_attr or num_tr_attr or str_ev_attr or num_ev_attr:
            columns = list(set(["case:" + x for x in str_tr_attr]).union(set(["case:" + x for x in num_tr_attr])).union(
                set(str_ev_attr)).union(set(num_ev_attr)))
            fea_df = dataframe_utils.get_features_df(log, columns, parameters=parameters)
            feature_names = list(fea_df.columns)
        else:
            fea_df = dataframe_utils.automatic_feature_extraction_df(log, parameters=parameters)
            feature_names = list(fea_df.columns)
        return fea_df, feature_names
    else:
        log = converter.apply(log, parameters=parameters)
        if str_tr_attr or num_tr_attr or str_ev_attr or num_ev_attr:
            return get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr,
                                      str_evsucc_attr=str_evsucc_attr, feature_names=feature_names)
        else:
            return get_default_representation(log, parameters=parameters)