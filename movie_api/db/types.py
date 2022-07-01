from movie_api.core.types import EnumClass


class SurveyQuestionType(EnumClass):
    free_text = "free-text"
    multiple_choice = "multiple-choice"
    # linear scale is 0 - 10 with changable label
    linear_scale = "linear-scale"
    # likert scale is 0 - 5 with static label
    likert_scale = "likert-scale"


class SurveyPublishType(EnumClass):
    immediate = "immediate"
    scheduled = "scheduled"


class SurveyPulseFrequencyType(EnumClass):
    weekly = "weekly"
    biweekly = "biweekly"
    monthly = "monthly"


class SurveyPulseRepeatedOnType(EnumClass):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6


class SurveyPulseRepeatedOnType(EnumClass):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6


class SurveyPulseRepeatedOnWeekType(EnumClass):
    first = 1
    second = 2
    third = 3
    fourth = 4
