import requests
import random
from os.path import exists, join
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.parse import match_one
from mycroft.util import resolve_resource_file
from space import next_cool_thing, astronauts_in_space, iss
from space.satellites import probe_distances
from space.bodies.exoplanets import all_cold_zone_planets, \
    all_confirmed_planets, all_exoplanet_around_a_stars, \
    all_exoplanet_around_b_stars, all_exoplanet_around_f_stars, \
    all_exoplanet_around_g_stars, all_exoplanet_around_k_stars, \
    all_exoplanet_around_m_stars, all_exoplanet_around_o_stars, \
    all_hot_zone_planets, all_jovian_planets, all_neptunian_planets, \
    all_subterran_planets, all_superterran_planets, all_terran_planets, \
    all_unconfirmed_planets, all_warm_zone_planets, \
    stars_known_to_host_exoplanets, confirmed_planets_that_transit_host_stars

__author__ = "JarbasAI"


class SpaceIsAwesome(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.cool_thing_cache = None
        self.astronauts_cache = None
        self.probe_cache = None
        self.terran_planets_cache = None
        self.subterran_planets_cache = None
        self.superterran_planets_cache = None
        self.jovian_planets_cache = None
        self.neptunian_planets_cache = None

        self.warm_zone_planets_cache = None
        self.hot_zone_planets_cache = None
        self.cold_zone_planets_cache = None

        self.a_star_planets_cache = None
        self.b_star_planets_cache = None
        self.f_star_planets_cache = None
        self.k_star_planets_cache = None
        self.m_star_planets_cache = None
        self.o_star_planets_cache = None
        self.g_star_planets_cache = None

        self.confirmed_planets_cache = None
        self.unconfirmed_planets_cache = None

        self.star_planets_cache = None

    @property
    def topics(self):
        voc_filename = "topics"
        lang = self.lang
        cache_key = lang + voc_filename
        if cache_key not in self.voc_match_cache:
            # Check for both skill resources and mycroft-core resources
            voc = self.find_resource(voc_filename + '.voc', 'vocab')
            if not voc:
                voc = resolve_resource_file(join('text', lang,
                                                 voc_filename + '.voc'))

            if not voc or not exists(voc):
                raise FileNotFoundError(
                    'Could not find {}.voc file'.format(voc_filename))

            with open(voc) as f:
                self.voc_match_cache[cache_key] = f.read().splitlines()
        return self.voc_match_cache[cache_key]

    @intent_handler(IntentBuilder("ProbeNamesIntent")
                    .require("names").require("probes"))
    def handle_probe_names(self, message):
        if self.probe_cache is None:
            self.probe_cache = probe_distances()["spaceprobe_distances"]
        names = " ".join(self.probe_cache.keys()).replace("_", " ").replace(
            "-", " ")
        self.speak_dialog("probe.names", {"names": names})

    @intent_handler(IntentBuilder("ProbeNumberIntent")
                    .require("how_many").require("probes"))
    def handle_probe_number(self, message):
        if self.probe_cache is None:
            self.probe_cache = probe_distances()["spaceprobe_distances"]
        number = len(self.probe_cache)
        self.speak_dialog("probe.number", {"number": number})

    @intent_file_handler('available.topics.intent')
    def handle_topics(self, message):
        topics = " ".join([t.replace("_", " ") for t in self.topics])
        self.speak_dialog("available.topics.dialog", {"topics": topics})

    @intent_file_handler('space.fact.intent')
    def handle_random_fact(self, message):
        topic = random.choice(self.topics).replace(" ", "_") + "_facts"
        self.speak_dialog(topic)

    @intent_file_handler('stars.planets.number.intent')
    def handle_number_of_stars_with_planets(self, message):
        if self.star_planets_cache is None:
            self.star_planets_cache = stars_known_to_host_exoplanets()
        self.speak_dialog("stars.with.planets",
                          {"number": len(self.star_planets_cache)})

    @intent_handler(IntentBuilder("StarsExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("orbiting").require("star"))
    def handle_number_of_star_planets(self, message):
        utterance = message.data["utterance"]
        if "type a" in utterance or "a type" in utterance or self.voc_match(
                utterance, "ATypeStar"):
            if self.a_star_planets_cache is None:
                self.a_star_planets_cache = all_exoplanet_around_a_stars[
                    "exoplanets"]
            number = len(self.a_star_planets_cache)
            star_type = "a"
        elif "type b" in utterance or "b type" in utterance or \
                self.voc_match(utterance, "BTypeStar"):
            if self.b_star_planets_cache is None:
                self.b_star_planets_cache = all_exoplanet_around_b_stars[
                    "exoplanets"]
            number = len(self.b_star_planets_cache)
            star_type = "b"
        elif "type f" in utterance or "f type" in utterance or \
                self.voc_match(utterance, "FTypeStar"):
            if self.f_star_planets_cache is None:
                self.f_star_planets_cache = all_exoplanet_around_f_stars[
                    "exoplanets"]
            number = len(self.f_star_planets_cache)
            star_type = "f"
        elif "type k" in utterance or "k type" in utterance or \
                self.voc_match(utterance, "KTypeStar"):
            if self.k_star_planets_cache is None:
                self.k_star_planets_cache = all_exoplanet_around_k_stars[
                    "exoplanets"]
            number = len(self.k_star_planets_cache)
            star_type = "k"
        elif "type m" in utterance or "m type" in utterance or \
                self.voc_match(utterance, "MTypeStar"):
            if self.m_star_planets_cache is None:
                self.m_star_planets_cache = all_exoplanet_around_m_stars[
                    "exoplanets"]
            number = len(self.m_star_planets_cache)
            star_type = "m"
        elif "type o" in utterance or "o type" in utterance or \
                self.voc_match(utterance, "OTypeStar"):
            if self.o_star_planets_cache is None:
                self.o_star_planets_cache = all_exoplanet_around_o_stars[
                    "exoplanets"]
            number = len(self.o_star_planets_cache)
            star_type = "o"
        elif "type g" in utterance or "g type" in utterance or \
                self.voc_match(utterance, "GTypeStar"):
            if self.g_star_planets_cache is None:
                self.g_star_planets_cache = all_exoplanet_around_g_stars[
                    "exoplanets"]
            number = len(self.g_star_planets_cache)
            star_type = "g"
        else:
            # TODO cache like the rest
            number = len(confirmed_planets_that_transit_host_stars())
            star_type = "any"

        self.speak_dialog("planet.orbiting.star.number",
                          {"number": number, "type": star_type})

    @intent_handler(IntentBuilder("HotZoneExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("hot_zone"))
    def handle_number_of_hot_zone_planets(self, message):
        if self.hot_zone_planets_cache is None:
            self.hot_zone_planets_cache = all_hot_zone_planets()[
                "exoplanets"]
        number = len(self.hot_zone_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "hot zone"})

    @intent_handler(IntentBuilder("ColdZoneExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("cold_zone"))
    def handle_number_of_cold_zone_planets(self, message):
        if self.cold_zone_planets_cache is None:
            self.cold_zone_planets_cache = all_cold_zone_planets()[
                "exoplanets"]
        number = len(self.cold_zone_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "cold zone"})

    @intent_handler(IntentBuilder("WarmZoneExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("warm_zone"))
    def handle_number_of_warm_zone_planets(self, message):
        if self.warm_zone_planets_cache is None:
            self.warm_zone_planets_cache = all_warm_zone_planets()[
                "exoplanets"]
        number = len(self.warm_zone_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "warm zone"})

    @intent_handler(IntentBuilder("NeptunianExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("neptunian"))
    def handle_number_of_neptunian_planets(self, message):
        if self.neptunian_planets_cache is None:
            self.neptunian_planets_cache = all_neptunian_planets()[
                "exoplanets"]
        number = len(self.neptunian_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "neptunian"})

    @intent_handler(IntentBuilder("JovianExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("jovian"))
    def handle_number_of_jovian_planets(self, message):
        if self.jovian_planets_cache is None:
            self.jovian_planets_cache = all_jovian_planets()[
                "exoplanets"]
        number = len(self.jovian_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "jovian"})

    @intent_handler(IntentBuilder("TerranExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("terran"))
    def handle_number_of_terran_planets(self, message):
        if self.terran_planets_cache is None:
            self.terran_planets_cache = all_terran_planets()[
                "exoplanets"]
        number = len(self.terran_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "terran"})

    @intent_handler(IntentBuilder("SuperterranExoplanetsIntent")
                    .require("how_many").optionally("exoplanets")
                    .require("superterran"))
    def handle_number_of_superterran_planets(self, message):
        if self.terran_planets_cache is None:
            self.terran_planets_cache = all_superterran_planets()[
                "exoplanets"]
        number = len(self.terran_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "superterran"})

    @intent_handler(IntentBuilder("SubterranExoplanetsIntent")
                    .require("how_many").op("exoplanets")
                    .require("subterran"))
    def handle_number_of_subterran_planets(self, message):
        if self.terran_planets_cache is None:
            self.terran_planets_cache = all_subterran_planets()[
                "exoplanets"]
        number = len(self.terran_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "subterran"})

    @intent_handler(IntentBuilder("ConfirmedExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("confirmed"))
    def handle_number_of_confirmed_planets(self, message):
        if self.confirmed_planets_cache is None:
            self.confirmed_planets_cache = all_confirmed_planets()
        number = len(self.confirmed_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "confirmed"})

    @intent_handler(IntentBuilder("UnconfirmedExoplanetsIntent")
                    .require("how_many").require("exoplanets")
                    .require("unconfirmed"))
    def handle_number_of_unconfirmed_planets(self, message):
        if self.unconfirmed_planets_cache is None:
            self.unconfirmed_planets_cache = all_unconfirmed_planets()
        number = len(self.unconfirmed_planets_cache)
        self.speak_dialog("planet.number",
                          {"number": number, "type": "unconfirmed"})

    @intent_file_handler('iss.intent')
    def handle_iss(self, message):
        iss_data = iss()
        lat = iss_data["iss_position"]["latitude"]
        lon = iss_data["iss_position"]["longitude"]
        user = self.settings.get("username", "demo")

        ocean_geo_names_req = "http://api.geonames.org/oceanJSON?lat=" + lat \
                              + "&lng=" + lon + "&username=" + user
        land_geo_names_req = "http://api.geonames.org/countryCodeJSON?formatted=true" \
                             "&lat=" + lat + "&lng=" + lon + "&username=" + user \
                             + "&style=full"

        try:
            land_geo_names_res = requests.get(land_geo_names_req)
            toponym_obj = land_geo_names_res.json()
            if toponym_obj.get("status", {}).get("value", 0) == 15:
                ocean_geo_names_res = requests.get(ocean_geo_names_req)
                toponym_obj = ocean_geo_names_res.json()
                toponym = "the " + toponym_obj['ocean']['name']
            else:
                toponym = toponym_obj['countryName']
        except:
            toponym = "unknown"
        if toponym == "unknown":
            self.speak_dialog("iss.location.unknown",
                              {"latitude": lat, "longitude": lon})
        else:
            self.speak_dialog("iss.location",
                              {"latitude": lat, "longitude": lon,
                               "toponym": toponym})

    @intent_file_handler('astronaut.names.intent')
    @intent_handler(IntentBuilder("AstronautIntent").require("names").require(
        "AstronautContext").require("question"))
    def handle_astronaut_names(self, message):
        if self.astronauts_cache is None:
            self.astronauts_cache = astronauts_in_space()
        for entry in self.astronauts_cache["people"]:
            name = entry["name"]
            craft = entry["craft"]
            self.speak_dialog("on.board",
                              {"name": name, "craft": craft}, wait=True)

    @intent_file_handler('astronaut.number.intent')
    def handle_astronaut_number(self, message):
        if self.astronauts_cache is None:
            self.astronauts_cache = astronauts_in_space()
        self.speak_dialog("astronaut.number",
                          {"number": self.astronauts_cache["number"]})
        # enable follow up question "who are they"/"what is their
        # name"/"what are they named" ....
        self.set_context("AstronautContext")

    @intent_file_handler('cool.thing.intent')
    def handle_next_cool_thing(self, message):
        if self.cool_thing_cache is None:
            space_thing = next_cool_thing()
            self.cool_thing_cache = space_thing["description"]
        self.speak(self.cool_thing_cache)

    @intent_file_handler('probe.distance.intent')
    def handle_probe_distance(self, message):
        if self.probe_cache is None:
            self.probe_cache = probe_distances()["spaceprobe_distances"]
        probe = match_one(message.data["probe"].strip().replace(" ", "-"),
                          list(
                              self.probe_cache.keys()))
        distance = float(self.probe_cache[probe].lower())
        self.speak_dialog("probe.distance",
                          {"distance": distance, "probe": probe})


def create_skill():
    return SpaceIsAwesome()
