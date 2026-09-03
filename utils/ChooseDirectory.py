
from pathlib import Path

from plyer import filechooser

import config

def ChooseDirectory(
    title: str = "Choose Directory",
    on_selected=lambda directory: print(f"Selected directory: {directory}")
) -> None:

    match config.platform():

        case "android":

            from jnius import autoclass
            from android import activity

            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            REQUEST_CODE = 100

            intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

            intent.addFlags(
                Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION
            )

            def on_activity_result(
                request_code,
                result_code,
                result_intent
            ):
                if request_code != REQUEST_CODE:
                    return

                # Unbind callback once we're finished.
                activity.unbind(
                    on_activity_result=on_activity_result
                )

                # RESULT_OK
                if result_code != -1 or result_intent is None:
                    if on_selected:
                        on_selected(None)
                    return

                uri = result_intent.getData()

                if uri is None:
                    if on_selected:
                        on_selected(None)
                    return

                # Persist access to the selected directory.
                flags = (
                    result_intent.getFlags()
                    & (
                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                        | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                    )
                )

                try:
                    PythonActivity.mActivity \
                        .getContentResolver() \
                        .takePersistableUriPermission(
                            uri,
                            flags
                        )
                except Exception as e:
                    print(
                        f"Could not persist directory permission: {e}"
                    )

                directory_uri = uri.toString()

                print(
                    f"Selected Android directory: {directory_uri}"
                )

                if on_selected:
                    on_selected(directory_uri)

            activity.bind(
                on_activity_result=on_activity_result
            )

            PythonActivity.mActivity.startActivityForResult(
                intent,
                REQUEST_CODE
            )

            return None

        # Works for desktop (Windows, Linux and Mac)
        case _:

            directories = filechooser.choose_dir(
                title=title
            )

            if not directories:
                return None

            directory = Path(directories[0])

            testFile = directory / ".permission_test"

            try:
                testFile.write_text("", encoding="utf-8")
                testFile.unlink()

            except OSError:
                return None

            if on_selected:
                on_selected(directory)
