import pytest
from em_parser import Parser


test_sample_cases = [
    # (campaign_name, airline_code, expected campaign type),
    # -----------------------------------------------------------------------------
    # Competitor.
    # -----------------------------------------------------------------------------
    (r'GS:en-US_CO=SteamshipAuthority/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=HylineCruises/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=SeastreakFerryNewBedford/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=SteamshipAuthority/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=IslandQueen/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=DartmouthCoach/Geo@US-Bus', 'Competitor')
]


class TestCampaignTypes:

    @pytest.mark.parametrize('campaign_name,campaign_type', test_sample_cases)
    def test_competitor(self, campaign_name, campaign_type):
        result = Parser(cached=False).parse(campaign_name)
        assert result['CampaignType'] == campaign_type
