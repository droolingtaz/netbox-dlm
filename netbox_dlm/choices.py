from utilities.choices import ChoiceSet


class HashingAlgorithmChoices(ChoiceSet):
    key = "SoftwareImageFile.hashing_algorithm"

    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"

    CHOICES = [
        (MD5, "MD5"),
        (SHA1, "SHA1"),
        (SHA256, "SHA256"),
        (SHA512, "SHA512"),
    ]


class ContractSupportLevelChoices(ChoiceSet):
    key = "Contract.support_level"

    BASIC = "basic"
    STANDARD = "standard"
    ENHANCED = "enhanced"
    PREMIUM = "premium"
    NEXT_BUSINESS_DAY = "next_business_day"
    FOUR_HOUR = "four_hour_onsite"
    NONE = "none"

    CHOICES = [
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (ENHANCED, "Enhanced"),
        (PREMIUM, "Premium"),
        (NEXT_BUSINESS_DAY, "Next Business Day"),
        (FOUR_HOUR, "4-Hour Onsite"),
        (NONE, "None"),
    ]


class CVESeverityChoices(ChoiceSet):
    key = "CVE.severity"

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    CHOICES = [
        (NONE, "None", "gray"),
        (LOW, "Low", "blue"),
        (MEDIUM, "Medium", "yellow"),
        (HIGH, "High", "orange"),
        (CRITICAL, "Critical", "red"),
    ]


class CVEStatusChoices(ChoiceSet):
    key = "CVE.status"

    AWAITING_REVIEW = "awaiting_review"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

    CHOICES = [
        (AWAITING_REVIEW, "Awaiting Review", "cyan"),
        (IN_REVIEW, "In Review", "blue"),
        (RESOLVED, "Resolved", "green"),
        (FALSE_POSITIVE, "False Positive", "gray"),
    ]


class VulnerabilityStatusChoices(ChoiceSet):
    key = "Vulnerability.status"

    OPEN = "open"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    ACCEPTED_RISK = "accepted_risk"
    IGNORED = "ignored"

    CHOICES = [
        (OPEN, "Open", "red"),
        (MITIGATED, "Mitigated", "yellow"),
        (RESOLVED, "Resolved", "green"),
        (ACCEPTED_RISK, "Accepted Risk", "purple"),
        (IGNORED, "Ignored", "gray"),
    ]
