from chatbot.core_bot import TrinetraBot


def test_chatbot_basic_flow_works_without_llm():
    profile = {
        "name": "Test Farmer",
        "land_size": 5.0,
        "soil_type": "Black Cotton",
        "budget": 50000,
        "location": "Hyderabad",
    }
    bot = TrinetraBot(language="English", farmer_profile=profile)

    response = bot.get_response("What are the current rice prices?")

    assert isinstance(response, str)
    assert len(response.strip()) > 0
    assert "rice" in response.lower() or "market" in response.lower() or "price" in response.lower()
