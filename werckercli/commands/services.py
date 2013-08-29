import math
import os
import re

from yaml import load
import semantic_version

from werckercli.client import Client
from werckercli.cli import get_term, puts
from werckercli.config import DEFAULT_WERCKER_YML


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
                versions = service.get("versionNumbers")
                if len(versions):
                    detailName = service["fullname"]
                    paddedName = detailName.ljust(pad_length)

                    if name:
                        paddedName = paddedName.replace(
                            name,
                            term.bold_white + name + term.normal
                        )

                    description = service["latestDescription"]
                    if description is None:
                        description = ""

                    versions = sorted(
                        versions,
                        key=lambda version: semantic_version.Version(version)
                    )

                    version = versions[len(versions)-1]
                    version = str(version)
                    version = version.rjust(8)
                    if name:
                        description = description.replace(
                            name,
                            term.bold_white + name + term.normal
                        )

                    puts(
                        paddedName + " - " + version + " - " +
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


def check_services(services):

    term = get_term()
    c = Client()

    response, result = c.get_boxes()

    for service in services:
        # print len(service)
        if len(service.splitlines()) > 1:
            puts("""{t.yellow}Warning:{t.normal} Incorrect service \
specification detected.
Reason: A new line detected in declaration:
{service}""".format(t=term, service=service))

        else:
            unversioned_patterned = "(?P<owner>.*)/(?P<name>.*)"
            versioned_pattern = "(?P<owner>.*)/(?P<name>.*)@(?P<version>.*)"

            results = re.search(versioned_pattern, service)

            if not results:
                results = re.search(unversioned_patterned, service)

            info_dict = results.groupdict()

            if not result:
                puts("""{t.red}Error:{t.normal}""".format(t=term))
            else:
                fullname = "{owner}/{name}".format(
                    owner=info_dict.get("owner"),
                    name=info_dict.get("name")
                )

                boxes = filter(
                    lambda box: box.get("fullname") == fullname,
                    result
                )

                # print boxes
                # print "Check"
                if len(boxes) == 0:
                    puts("""{t.yellow}Warning:{t.normal} Service \
{fullname} not found.""".format(
                        t=term)
                    )

                else:
                    box = boxes[0]
                    versions = box.get("versionNumbers", [])

                    versions = sorted(
                        versions,
                        key=lambda version: semantic_version.Version(version)
                    )

                    latest_version = False
                    requested_version = info_dict.get("version", None)

                    if not requested_version:
                        version_found = len(versions) > 0
                        # latest_version = versions[len(versions)-1]
                        requested_version = versions[len(versions)-1]
                    else:

                        version_found = False

                        requested_version = semantic_version.Version(
                            requested_version
                        )

                        for version in versions:
                            sem_ver = semantic_version.Version(version)
                            # print sem_ver, requested_version
                            if requested_version < sem_ver:
                                latest_version = sem_ver
                            elif requested_version == sem_ver:
                                version_found = True

                    if version_found is False:
                        info = "{t.red}not found{t.normal}".format(
                            t=term
                        )
                    elif latest_version is not False:
                        info = "{t.yellow}upgrade to {sem_ver}{t.normal}".\
                            format(
                                t=term,
                                sem_ver=latest_version
                            )
                    else:
                        info = "{t.green}latest{t.normal}".format(t=term)
                    puts(
                        "{fullname} - {version} ({info}) - {description}".
                        format(
                            fullname=fullname,
                            info=info,
                            version=requested_version,
                            description=box.get("latestDescription")
                        )
                    )


def list_services(path='.'):
    # pass
    yaml = os.path.join(path, DEFAULT_WERCKER_YML)

    term = get_term()

    if os.path.isfile(yaml):
        fh = open(yaml)
        data = fh.read()

        yaml_data = load(data)

        services = yaml_data.get("services")

        if not services:
            puts(
                "{t.yellow}Warning:{t.normal} No services specified in the \
{yaml}".
                format(
                    yaml=DEFAULT_WERCKER_YML,
                    t=term
                )
            )
        else:
            if type(services) is str:
                services = [services]

            puts("Services currently in use:")
            check_services(services)
            # puts("Services currently specified:")
            # puts(",\n".join(services))

                    # print len(boxes)
                    # print results.groupdict()

    else:
        puts("{t.red}Error:{t.normal} {yaml} not found".format(
            yaml=DEFAULT_WERCKER_YML,
            t=term)
        )
