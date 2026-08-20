
import sys

def isPythonRightVersion(
    requiredMajorVersion: int | None = None,
    requiredMinorVersion: int | None = None,
    requiredMicroVersion: int | None = None,
    throw: bool = True
) -> bool:

    REQUIRED_MAJOR = requiredMajorVersion
    REQUIRED_MINOR = requiredMinorVersion
    REQUIRED_MICRO = requiredMicroVersion

    CURRENT_MAJOR = sys.version_info.major
    CURRENT_MINOR = sys.version_info.minor
    CURRENT_MICRO = sys.version_info.micro

    isRightVersion = False

    if (REQUIRED_MAJOR is not None) and (REQUIRED_MAJOR != CURRENT_MAJOR):
        isRightVersion = False
    elif (REQUIRED_MINOR is not None) and (REQUIRED_MINOR != CURRENT_MINOR):
        isRightVersion = False
    elif (REQUIRED_MICRO is not None) and (REQUIRED_MICRO != CURRENT_MICRO):
        isRightVersion = False
    else:
        isRightVersion = True

    if not isRightVersion:

        def version_number_to_str(version: int | None) -> str:
            if version is None:
                return "x"
            return str(version)

        REQUIRED_MAJOR_STR = version_number_to_str(REQUIRED_MAJOR)
        REQUIRED_MINOR_STR = version_number_to_str(REQUIRED_MINOR)
        REQUIRED_MICRO_STR = version_number_to_str(REQUIRED_MICRO)

        CURRENT_MAJOR_STR = version_number_to_str(CURRENT_MAJOR)
        CURRENT_MINOR_STR = version_number_to_str(CURRENT_MINOR)
        CURRENT_MICRO_STR = version_number_to_str(CURRENT_MICRO)

        print(
            f"\nERROR: This build script must be run with Python "
            f"{REQUIRED_MAJOR_STR}.{REQUIRED_MINOR_STR}.{REQUIRED_MICRO_STR}"
            f" You are using {CURRENT_MAJOR_STR}.{CURRENT_MINOR_STR}.{CURRENT_MICRO_STR}"
        )
        if throw:
            raise Exception("")

    return isRightVersion
