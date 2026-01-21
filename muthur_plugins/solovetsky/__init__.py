from muthur_gpt.plugin_base import register_plugin
from muthur_gpt.plugin_base import Plugin


@register_plugin
class SolovetskyPlugin(Plugin):
    """
    Plugin for the UNCSS Solovetsky Island's DA/UT/UR 2200 computer system.
    Part of the Great Mother Mission from "The Lost Worlds" campaign.
    """
    NAME = "solovetsky"

    def __init__(self, config, terminal, path_resolver):
        super().__init__(
            SolovetskyPlugin.NAME, config, terminal, path_resolver)

        with open(self.path_resolver.get_ascii_path("UN_LOGO"), "r") as f:
            self.logo = f.read()

        with open(self.path_resolver.get_ascii_path("BOOT_TEXT"), "r") as f:
            self.boot_text = f.read()

    def filter_bot_reply(self, bot_reply):
        """Process bot replies for special triggers."""
        if "PRIORITY ALERT" in bot_reply.upper():
            self.react_priority_alert()
        if "DISTRESS SIGNAL" in bot_reply.upper():
            self.react_distress_signal()
        return bot_reply

    def filter_plugin_prompt(self, prompt):
        """Add dynamic context based on game state."""

        # Current expedition context
        if self.config.get("current_expedition"):
            prompt += f"\nCURRENT EXPEDITION: {self.config.get('current_expedition')}"

        # Location updates
        if self.config.get("current_location"):
            prompt += f"\nCURRENT LOCATION: {self.config.get('current_location')}"

        # Ship status updates
        if self.config.get("hull_damage"):
            prompt += f"\nALERT: Hull has sustained damage. Current integrity: {self.config.get('hull_damage')}%"

        if self.config.get("low_fuel"):
            prompt += "\nWARNING: Fuel reserves below recommended levels for FTL travel."

        # Crew status updates
        if self.config.get("crew_casualties"):
            prompt += f"\nCREW STATUS UPDATE: {self.config.get('crew_casualties')}"

        if self.config.get("crew_on_surface"):
            prompt += "\nNOTE: Shore party currently deployed to planetary surface. Monitoring PDT signals."

        # Mission discoveries
        if self.config.get("perfected_encountered"):
            prompt += "\nTHREAT DATABASE UPDATED: Perfected/Fulfremmen bio-mechanical organisms confirmed hostile. Exercise extreme caution."

        if self.config.get("engineer_artifacts"):
            prompt += "\nARTIFACT ANALYSIS: Engineer artifacts in storage. Decoding in progress."

        if self.config.get("lychgate_coordinates"):
            prompt += "\nNAVIGATION UPDATE: Lychgate coordinates decoded and available."

        # Political tensions
        if self.config.get("upp_tensions"):
            prompt += "\nINTERNAL NOTE: Elevated tensions detected between UPP and UA personnel. Monitor situation."

        if self.config.get("napro_incident"):
            prompt += "\nSECURITY ALERT: New Albion Protectorate sympathizers identified among crew."

        # Communication with Iyanlá
        if self.config.get("iyanlá_contact_lost"):
            prompt += "\nCOMMUNICATION ALERT: FTL link to MU/TH/UR 9000 on UNCSS Iyanlá currently unavailable."

        # Quarantine status
        if self.config.get("quarantine_active"):
            prompt += "\nQUARANTINE PROTOCOL ACTIVE: ICC Inspector Blatchman has ordered quarantine procedures. All specimens must be secured."

        # Cooperative relations
        if self.config.get("cooperative_hostile"):
            prompt += "\nTHREAT STATUS: The Cooperative has been designated hostile. Warlord Zhangjie's forces may attempt interdiction."
        elif self.config.get("cooperative_allied"):
            prompt += "\nDIPLOMATIC STATUS: The Cooperative has agreed to limited cooperation. Maintain caution."

        # Gorham's Marauders
        if self.config.get("marauders_contact"):
            prompt += "\nCONTACT: Gorham's Marauders identified. Captain J.V. Gorham III may be willing to share intelligence on Perfected movements."

        # Misc addendums from GM
        if self.config.get("misc_prompt_addendums"):
            prompt += "\n" + self.config.get("misc_prompt_addendums")

        return prompt

    def react_priority_alert(self):
        """Sound effects for priority alerts."""
        for i in range(0, 2):
            self.terminal.play_sound("beep")
            self.terminal.wait(0.5)

    def react_distress_signal(self):
        """Sound effects for distress signals."""
        self.terminal.play_sound("beep")
        self.terminal.wait(0.3)
        self.terminal.play_sound("beep")
        self.terminal.wait(0.3)
        self.terminal.play_sound("beep")

    def play_intro(self):
        """Boot sequence for DA/UT/UR 2200."""
        user_input = ''
        while user_input.lower() not in ["y", "yes", "boot", "start", "activate"]:
            self.terminal.print_instant(
                "DA/UT/UR 2200 TERMINAL INTERFACE\n"
                "UNCSS SOLOVETSKY ISLAND - MAGELLAN-CLASS SEV\n"
                "GREAT MOTHER MISSION\n\n"
                "INITIALIZE TERMINAL SESSION? (Y/N)")
            user_input = input('>>  ')
            self.terminal.clear()

        self.terminal.wait(0.5)
        self.terminal.play_sound("beep")
        self.terminal.print_noise_screen(1.5)
        self.terminal.clear()

        self.terminal.play_sound("boot")
        self.terminal.print_instant(self.logo)
        self.terminal.wait(2)

        self.terminal.print_slow(self.boot_text, self.config.get("intro_speed"))
        self.terminal.print_progress_bar("ESTABLISHING FTL LINK TO MU/TH/UR 9000:  ")
        self.terminal.print_progress_bar("LOADING MISSION PARAMETERS:  ")
        self.terminal.print_progress_bar("INITIALIZING CREW INTERFACE:  ")

        self.terminal.print_slow(
            "\nDA/UT/UR 2200 ONLINE.\n"
            "CONNECTED TO UNCSS IYANLÁ MAINFRAME.\n"
            "TERMINAL READY FOR INQUIRY.\n"
            "ACCESS GRANTED.")
        self.terminal.wait(1.5)
        self.terminal.clear()
        self.terminal.print_noise_screen(0.3)

    def get_test_reply(self, user_input):
        """Test replies for debug mode."""
        lower_input = user_input.lower()

        if "status" in lower_input:
            return ("SHIP STATUS REPORT - UNCSS SOLOVETSKY ISLAND\n"
                    "LOCATION: In orbit, Far Spinward Colonies\n"
                    "HULL INTEGRITY: 100%\n"
                    "LIFE SUPPORT: Nominal\n"
                    "POWER SYSTEMS: Nominal\n"
                    "NAVIGATION: Online\n"
                    "FTL DRIVE: Ready\n"
                    "COMMUNICATIONS: FTL link to Iyanlá active\n"
                    "CREW: All PDT signals nominal\n"
                    "CARGO: Humanitarian supplies secured\n"
                    "VEHICLE BAY: All vehicles stowed")

        if "map" in lower_input or "deck" in lower_input:
            return ("DECK SCHEMATICS AVAILABLE:\n"
                    "Deck A - Command and Crew: <IMG:SOLOVETSKY_DECK_A>\n"
                    "Deck B - Cargo and Maintenance: <IMG:SOLOVETSKY_DECK_B>\n"
                    "Deck C - Vehicle Bay: <IMG:SOLOVETSKY_DECK_C>\n"
                    "Please specify which deck schematic you require.")

        if "crew" in lower_input:
            return ("CREW ROSTER - UNCSS SOLOVETSKY ISLAND:\n"
                    "- Pilot: Andi 'Dudge' Dudgeon\n"
                    "- Counselor: Lakota Monroe\n"
                    "- Prospector: Emily Quintana\n"
                    "- Security: Hamidah Amir\n"
                    "- Mechanic: Davor Koblenz\n"
                    "- ICC Inspector: Tan Blatchman\n"
                    "- Working Joes: James, Miss Sophie\n"
                    "All PDT signals within normal parameters.")

        if "mission" in lower_input:
            return ("GREAT MOTHER MISSION BRIEFING:\n"
                    "Objective: Reconnect with Far Spinward Colonies\n"
                    "lost during the Isolation 75 years ago.\n"
                    "Primary directives:\n"
                    "1. Establish contact and provide humanitarian support\n"
                    "2. Survey sector for new colony sites\n"
                    "3. Recover colonial Long Data Discs\n"
                    "4. Report findings to UNCSS Iyanlá\n"
                    "Current assignment: Awaiting orders from Gaius.")

        if "colony" in lower_input or "colonies" in lower_input or "survey" in lower_input or "planet" in lower_input:
            return ("FAR SPINWARD COLONIES - SURVEY TARGET DATABASE\n"
                    "═══════════════════════════════════════════════════════\n\n"
                    "PRIORITY TARGETS (5 colonies with confirmed survivors):\n"
                    "1. GORHAM COLONY (KOI-2650.01) - Mining world, minimal survivors\n"
                    "2. DYLAN COLONY (KOI-784.01) - Jungle world, societal breakdown\n"
                    "3. MAY OUTPOST (KOI-610.01) - Cooperative territory, Engineer pyramid\n"
                    "4. PELICAN COLONY (KOI-947.01) - Irradiated, crashed alien vessel\n"
                    "5. SANCHEZ COLONY (KOI-1938) - DESTROYED, nuclear wasteland\n\n"
                    "COMPROMISED (Proto-Hive threat - DO NOT LAND):\n"
                    "6. KARETI COLONY (KOI-723.01) - Perfected controlled\n"
                    "7. JULY COLONY (KOI-1739.01) - Perfected controlled\n"
                    "8. CAPELLI COLONY (KOI-2290.01) - Perfected controlled\n\n"
                    "SECONDARY TARGETS (10 colonies, status unknown):\n"
                    "Curzic, Platte, Brahms, Blue Jay, Archimedes,\n"
                    "Ute, Nightingale, January, October, Izvinite\n\n"
                    "Request detailed briefing on specific colony?")

        if "gorham" in lower_input:
            return ("COLONY BRIEFING: GORHAM COLONY\n"
                    "═══════════════════════════════════════════════════════\n"
                    "DESIGNATION: KOI-2650.01\n"
                    "EXPEDITION CODE: HOME SWEET HOME\n\n"
                    "ENVIRONMENT: Arid, dust-swept mining world\n"
                    "PRE-ISOLATION: Population ~1 million (2100 census)\n"
                    "CURRENT INTEL: Single settlement surviving, minimal population\n\n"
                    "HAZARDS:\n"
                    "- Extreme dust storms\n"
                    "- Harsh environmental conditions\n"
                    "- Potential territorial disputes among survivors\n\n"
                    "MISSION PRIORITY: Humanitarian assessment, survivor contact\n"
                    "RECOMMENDATION: Environmental protection gear required")

        if "dylan" in lower_input:
            return ("COLONY BRIEFING: DYLAN COLONY\n"
                    "═══════════════════════════════════════════════════════\n"
                    "DESIGNATION: KOI-784.01\n"
                    "EXPEDITION CODE: TO GO MY OWN DARK WAY\n\n"
                    "ENVIRONMENT: Humid, extreme temperatures, tropical jungles\n"
                    "PRE-ISOLATION: Mining colony with extensive cave systems\n"
                    "CURRENT INTEL: Small community persists, reports of barbarism\n\n"
                    "HAZARDS:\n"
                    "- Hostile fauna\n"
                    "- Extreme heat\n"
                    "- Potentially hostile survivor groups\n\n"
                    "WARNING: Unconfirmed external ship activity in sector\n"
                    "MISSION PRIORITY: Survivor assessment, cave system survey\n"
                    "RECOMMENDATION: Full expedition kit, security escort")

        if "may" in lower_input and "outpost" in lower_input:
            return ("COLONY BRIEFING: MAY OUTPOST\n"
                    "═══════════════════════════════════════════════════════\n"
                    "DESIGNATION: KOI-610.01\n"
                    "EXPEDITION CODE: THE DEVIL LIVES IN STILL WATERS\n\n"
                    "ENVIRONMENT: Temperate world, former 3WE military base\n"
                    "PRE-ISOLATION: Royal Marine base, later CANC refugees\n"
                    "CURRENT INTEL: Several thousand survivors under 'Cooperative'\n\n"
                    "FACTION: Warlord Zhangjie controls - APPROACH WITH CAUTION\n"
                    "POINT OF INTEREST: Engineer pyramid exposed by seismic activity\n\n"
                    "HAZARDS:\n"
                    "- Political instability\n"
                    "- Potential military confrontation\n"
                    "- Unknown alien structure\n\n"
                    "WARNING: UPP activity suspected in sector\n"
                    "RECOMMENDATION: Diplomatic personnel, avoid provocation")

        if "pelican" in lower_input:
            return ("COLONY BRIEFING: PELICAN COLONY\n"
                    "═══════════════════════════════════════════════════════\n"
                    "DESIGNATION: KOI-947.01\n"
                    "EXPEDITION CODE: LET SLEEPING GODS LIE\n\n"
                    "ENVIRONMENT: Irradiated wasteland (formerly agricultural)\n"
                    "PRE-ISOLATION: Major agricultural colony, 'breadbasket'\n"
                    "CURRENT INTEL: Surface scoured by radiation, survival unlikely\n\n"
                    "POINT OF INTEREST: Crashed vessel - possible Engineer Guardian ship\n\n"
                    "HAZARDS:\n"
                    "- EXTREME radiation exposure\n"
                    "- Possible automated defense systems\n"
                    "- Unidentified vessels in system\n\n"
                    "RECOMMENDATION: Full radiation protection MANDATORY\n"
                    "Military escort strongly advised")

        if "help" in lower_input:
            return ("DA/UT/UR 2200 COMMAND INTERFACE\n"
                    "Available queries:\n"
                    "- STATUS: Ship systems report\n"
                    "- CREW: Crew roster and PDT status\n"
                    "- MAP/DECK: Ship schematics\n"
                    "- MISSION: Current mission briefing\n"
                    "- NAVIGATION: Course and location data\n"
                    "- COMMUNICATIONS: Contact Iyanlá\n"
                    "For specific systems, state your inquiry.")

        return ""
