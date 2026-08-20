
def isPythonRightVersion(
    requiredMajorVersion: int = -1,
    requiredMinorVersion: int = -1,
    requiredMicroVersion: int = -1,
    throw: bool = True
) -> bool:

    REQUIRED_MAJOR = requiredMajorVersion
    REQUIRED_MINOR = requiredMajorVersion
    REQUIRED_MICRO = requiredMajorVersion

    CURRENT_MAJOR = sys.version_info.major
    CURRENT_MINOR = sys.version_info.minor
    CURRENT_MICRO = sys.version_info.micro

    isRightVersion = False

    if (REQUIRED_MAJOR != -1) and (REQUIRED_MAJOR != CURRENT_MAJOR):
        isRightVersion = False
    elif (REQUIRED_MINOR != -1) and (REQUIRED_MINOR != CURRENT_MINOR):
        isRightVersion = False
    elif (REQUIRED_MICRO != -1) and (REQUIRED_MICRO != CURRENT_MICRO):
        isRightVersion = False
    else:
        isRightVersion = True

    if not isRightVersion:

        def version_number_to_str(version: int) -> str:
            if version == -1:
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
