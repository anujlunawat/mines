import settings


def height_prct(percentage):
    return (settings.HEIGHT / 100) * percentage


def width_prct(percentage):
    return (settings.WIDTH / 100) * percentage


def height_prct_of_right_frame(percentage):
    '''
    made for cells_frame
    :param percentage:
    :return:
    '''
    return (height_prct(100) / 100) * percentage


def width_prct_of_right_frame(percentage):
    '''
    made for cells_frame
    :param percentage:
    :return:
    '''
    return (width_prct(75) / 100) * percentage


def center_frame_height_prct(percentage):
    return (height_prct(100) - height_prct_of_right_frame(75)) / (100 / percentage)


def center_frame_width_prct(percentage):
    return (width_prct(75) - width_prct_of_right_frame(75)) / (100 / percentage)


def any_prct(hw, percentage):
    return (hw / 100) * percentage

