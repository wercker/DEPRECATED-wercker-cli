import math

from werckercli.client import Client
from werckercli.cli import get_term, puts


def search_services(name):

    client = Client()

    term = get_term()

    response, results = client.get_boxes()

    if results and len(results):
        services = filter(
            lambda box: box.get("latestType", "") == "service",
            results
        )
        services = sorted(
            services,
            key=lambda service: service.get("fullname")
        )

        if name:
            services = filter(
                lambda box: (
                    box.get("fullname", "").find(name) != -1 or
                    box.get("latestDescription").find(name) != -1
                ),
                services
            )

        if len(services) is not 0:
            if term.width:
                pad_length = term.width * 0.2
                pad_length = int(math.floor(pad_length))
                pad_length = max(pad_length, 30)
                pad_length = min(pad_length, 50)
            else:
                pad_length = 0

            for service in services:
                detailName = service["fullname"]
                paddedName = detailName.ljust(pad_length)
                paddedName = paddedName.replace(
                    name,
                    term.bold_white + name + term.normal
                )

                description = service["latestDescription"]
                if description is None:
                    description = ""

                description = description.replace(
                    name,
                    term.bold_white + name + term.normal
                )

                puts(
                    paddedName + " - " +
                    description
                )

        else:
            if name:
                puts(
                    "No services found with: {t.bold_white}{0}{t.normal}".
                    format(
                        name,
                        t=term
                    )
                )
            else:
                puts("No services found.")


def putInfo(label, data, multiple_lines=False):
    term = get_term()

    paddedLabel = str(label) + ":"
    paddedLabel = paddedLabel.ljust(20)

    if multiple_lines is True:
        seperator = "\n"
    else:
        seperator = ""

    puts("{t.bold}{t.white}{label}{t.normal}{seperator}{data}".format(
        label=paddedLabel,
        seperator=seperator,
        data=data,
        t=term)
    )


def info_service(owner, name, version=0):

    client = Client()
    term = get_term()

    puts("Retrieving service: {t.bold_white}{owner}/{name}\n".format(
        owner=owner,
        name=name,
        t=term)
    )
    response, results = client.get_box(owner, name, version=version)

    if response == 404:
        puts(term.yellow("Warning: ") + "service not found.")
    elif results.get("type") != "service":
        puts(term.yellow("Warning: ") + "found box was not a service.")
    else:
        # print results.keys()
        # print results

        putInfo("Owner", results.get("owner"))
        putInfo("Name", results.get("name"))
        putInfo("Version", results.get("version"))
        license = results.get("license")
        if license is None:
            license = "none specified"
        putInfo("License", license)

        keywords = ", ".join(results.get("keywords"))
        if keywords is None:
            keywords = ""

        putInfo("Keywords", keywords)
        putInfo(
            "\nDescription",
            results.get("description"),
            multiple_lines=True
        )

        packages = ""
        for package in results.get("packages"):
            if len(packages):
                packages += ", "

            packages += "{name}: {version}".format(
                name=package.get("name"), version=package.get("version")
            )
        else:
            packages = "None specified"
        putInfo("\nPackages", packages, multiple_lines=True)
        putInfo("\nRead me", results.get("readMe"), multiple_lines=True)
        # puts("{t.bold}{t.white}releases:        {t.normal}\n{0}".format(
        #     ",\n".join(results.get("versions")),
        #     t=term)
        # )
        # puts("{t.bold}{t.white}")
