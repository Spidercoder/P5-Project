"""Functions for analysing aspects of the data. The analysis is used to make decision about data manipulation."""
import numpy as np
import datareader_csv


def get_mean_time_between_normal_messages(messages, remote_frame_and_response_indices):
    """Returns the mean time between normal message neighbours, ignoring remote frames and remote frame responses."""
    # The times between two normal messages.
    times_between_messages = []

    # Changing the list to a set to improve the time complexity of the "in" operation.
    remote_frame_and_response_indices = set(remote_frame_and_response_indices)

    # Using the list of non-normal indices to find the time between all neighbour pairs of normal messages.
    for i in range(len(messages) - 1):
        if i not in remote_frame_and_response_indices and i + 1 not in remote_frame_and_response_indices:
            times_between_messages.append(messages[i + 1].timestamp - messages[i].timestamp)

    return np.mean(times_between_messages)


def get_mean_time_between_split_messages(messages, remote_frame_and_response_indices):
    """Returns the mean time between message pairs that have a remote frame or remote frame response between them."""
    times_between_messages = []

    # Using the list of non-normal indices to find all neighbours of remote frames and remote frame responses.
    for index in remote_frame_and_response_indices:
        times_between_messages.append(messages[index + 1].timestamp - messages[index - 1].timestamp)

    return np.mean(times_between_messages) if len(times_between_messages) > 0 else 0


def __get_remote_frame_and_response_indices(messages):
    latest_remote_frame = None
    latest_remote_frame_index = None

    remote_frame_or_response_indices = []

    # Finding all the indices of the remote frames and remote frame responses
    for i in range(len(messages)):
        # If the message is a remote frame.
        if messages[i].rtr == 0b100:
            latest_remote_frame = messages[i]
            latest_remote_frame_index = i
            remote_frame_or_response_indices.append(i)
        # If it is a remote frame response.
        elif latest_remote_frame is not None and \
                messages[i].id == latest_remote_frame.id and i - latest_remote_frame_index < 7:
            latest_remote_frame = None
            latest_remote_frame_index = None
            remote_frame_or_response_indices.append(i)

    return remote_frame_or_response_indices


def analyze_messages(messages):
    """Returns a dictionary where the keys are descriptions of the information in the values"""
    remote_frame_and_response_indices = __get_remote_frame_and_response_indices(messages)

    information = {
        "Mean time between normal messages: ":
            get_mean_time_between_normal_messages(messages, remote_frame_and_response_indices),
        "Mean time between split messages: ":
            get_mean_time_between_split_messages(messages, remote_frame_and_response_indices),
    }

    return information


if __name__ == "__main__":
    file_messages = datareader_csv.load_attack_free1()

    print(analyze_messages(file_messages))

    # Without removing remote frames: 0.00042314722179202243
    # Removing remote frames without closing the holes: 0.00047852379197671924
    # Removing remote frames and closing the holes: 0.0004403009096925493

    # Average time between split messages: 0.0009379362399745852