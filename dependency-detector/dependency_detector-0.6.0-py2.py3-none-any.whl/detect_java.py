from os import path
from typing import List
from xml.dom.minidom import Element, parse

from detector.dependency import Dependency


def detect_java(directory_path: str) -> List[Dependency]:
    result: List[Dependency] = []
    possibly_pom_xml = f"{directory_path}/pom.xml"
    if path.exists(possibly_pom_xml):
        java_version = None
        dom = parse(possibly_pom_xml)
        properties_list = dom.getElementsByTagName("properties")
        if len(properties_list) > 0:
            for prop in properties_list[0].childNodes:
                if isinstance(prop, Element):
                    if prop.tagName == "java.version":
                        java_version = prop.firstChild.data

        if java_version is None:
            plugin_elements = dom.getElementsByTagName("plugin")
            for plugin_element in plugin_elements:
                artifactId = plugin_element.getElementsByTagName("artifactId")
                if (
                    len(artifactId) == 1
                    and artifactId[0].firstChild.data == "maven-compiler-plugin"
                ):
                    configuration = plugin_element.getElementsByTagName("configuration")
                    if len(configuration) == 1:
                        target = configuration[0].getElementsByTagName("target")
                        if len(target) == 1:
                            java_version = target[0].firstChild.data

        if java_version is None:
            # Default to java 11
            java_version = "11"

        if java_version == "1.8":
            result.append(Dependency.JAVA8)
        elif java_version == "11":
            result.append(Dependency.JAVA11)

        result.append(Dependency.MAVEN)
    return result
