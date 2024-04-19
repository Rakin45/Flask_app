from flask import url_for
from playwright.sync_api import expect
import re


def test_home_page_loads(live_server, page):
    page.goto(url_for('api_bp.home', _external=True))
    expect(page).to_have_title("Home | Water Quality Control")


def test_signup_login_flow(live_server, page):
    page.goto(url_for('api_bp.home', _external=True))
    
    page.get_by_role("link", name="Signup").click()
    expect(page).to_have_title("Signup | Water Quality Control")
    page.get_by_placeholder("jhondoe").click()
    page.get_by_placeholder("jhondoe").fill("user1")
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("user1@email.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_label("I agree to terms").check()
    page.get_by_role("button", name="Sign Up").click()
    
    
    page.get_by_role("link", name="Log In").click()
    expect(page).to_have_title("Login | Water Quality Control")
    page.get_by_placeholder("username").click()
    page.get_by_placeholder("username").fill("user1")
    page.get_by_placeholder("username").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Log In").click()
    expect(page).to_have_title("Dashboard | Water Quality Control")


def test_predict_water_quality(live_server, page):
    page.goto(url_for('api_bp.home', _external=True))
    page.get_by_role("link", name="Signup").click()
    page.get_by_placeholder("jhondoe").click()
    page.get_by_placeholder("jhondoe").fill("user1")
    page.get_by_placeholder("jhondoe").press("Tab")
    page.get_by_placeholder("name@example.com").fill("user1@email.com")
    page.get_by_placeholder("name@example.com").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_label("I agree to terms").check()
    page.get_by_role("button", name="Sign Up").click()
    page.get_by_role("link", name="Login").click()
    page.get_by_placeholder("username").click()
    page.get_by_placeholder("username").fill("user1")
    page.get_by_placeholder("username").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Log In").click()
    page.get_by_label("Specific Conductace Max").click()
    page.get_by_label("Specific Conductace Max").fill("30")
    page.get_by_label("Specific Conductace Min").click()
    page.get_by_label("Specific Conductace Min").fill("40")
    page.get_by_label("Specific Conductace Mean").click()
    page.get_by_label("Specific Conductace Mean").fill("35")
    page.get_by_label("PH Max").click()
    page.get_by_label("PH Max").fill("6")
    page.get_by_label("PH Max").click()
    page.get_by_label("PH Max").fill("8")
    page.get_by_label("PH Min").click()
    page.get_by_label("PH Min").fill("6")
    page.get_by_label("Dissolved O2 Min").click()
    page.get_by_label("Dissolved O2 Min").fill("6")
    page.get_by_label("Dissolved O2 Max").click()
    page.get_by_label("Dissolved O2 Max").fill("7")
    page.get_by_label("Dissolved O2 Max").click()
    page.get_by_label("Dissolved O2 Max").fill("8")
    page.get_by_label("Dissolved O2 Mean").click()
    page.get_by_label("Dissolved O2 Mean").fill("7")
    page.get_by_label("Tempreture Min").click()
    page.get_by_label("Tempreture Min").fill("30")
    page.get_by_label("Tempreture Mean").click()
    page.get_by_label("Tempreture Mean").fill("35")
    page.get_by_label("Tempreture Max").click()
    page.get_by_label("Tempreture Max").fill("40")
    
    training_field = page.locator('#training')
    training_field.select_option(value='1')  
    location_field = page.locator('#location')
    location_field.select_option(value='1')  
    page.get_by_role("button", name="Predict").click()
    
    expect(page.locator('body')).to_have_text(re.compile("Water Quality"))

    
def test_unauthorized_url(live_server, page):
    page.goto(url_for('api_bp.get_insights', _external=True))
    assert page.url.startswith(url_for('api_bp.login', _external=True)) or "Unauthorized" in page.content()
    page.goto(url_for('api_bp.dashboard', _external=True))
    assert page.url.startswith(url_for('api_bp.login', _external=True)) or "Unauthorized" in page.content()
    page.goto(url_for('api_bp.user_profile', _external=True))
    assert page.url.startswith(url_for('api_bp.login', _external=True)) or "Unauthorized" in page.content()
    page.goto(url_for('api_bp.get_predictions', _external=True))
    assert page.url.startswith(url_for('api_bp.login', _external=True)) or "Unauthorized" in page.content()
    

def test_authorized_url(live_server, page):
    page.goto(url_for('api_bp.home', _external=True))
    
    page.get_by_role("link", name="Signup").click()
    expect(page).to_have_title("Signup | Water Quality Control")
    page.get_by_placeholder("jhondoe").click()
    page.get_by_placeholder("jhondoe").fill("user1")
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("user1@email.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_label("I agree to terms").check()
    page.get_by_role("button", name="Sign Up").click()
    
    
    page.get_by_role("link", name="Log In").click()
    expect(page).to_have_title("Login | Water Quality Control")
    page.get_by_placeholder("username").click()
    page.get_by_placeholder("username").fill("user1")
    page.get_by_placeholder("username").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Log In").click()
    expect(page).to_have_title("Dashboard | Water Quality Control")
    page.get_by_role("link", name=" Predictions").click()
    expect(page).to_have_title("Predictions | Water Quality Control")
    page.get_by_role("link", name=" Insights").click()
    expect(page).to_have_title("Insights | Water Quality Control")
    page.get_by_role("link", name=" Profile").click()
    expect(page).to_have_title("Profile | Water Quality Control")


    
    

def test_logout(live_server, page):

    page.goto(url_for('api_bp.home', _external=True))
    
    page.get_by_role("link", name="Signup").click()
    expect(page).to_have_title("Signup | Water Quality Control")
    page.get_by_placeholder("jhondoe").click()
    page.get_by_placeholder("jhondoe").fill("user1")
    page.get_by_placeholder("name@example.com").click()
    page.get_by_placeholder("name@example.com").fill("user1@email.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_label("I agree to terms").check()
    page.get_by_role("button", name="Sign Up").click()
    
    
    page.get_by_role("link", name="Log In").click()
    expect(page).to_have_title("Login | Water Quality Control")
    page.get_by_placeholder("username").click()
    page.get_by_placeholder("username").fill("user1")
    page.get_by_placeholder("username").press("Tab")
    page.get_by_placeholder("Password").fill("12345678")
    page.get_by_role("button", name="Log In").click()
    expect(page).to_have_title("Dashboard | Water Quality Control")

    page.get_by_role("link", name="u user1 ").click()
    page.get_by_role("link", name="Log Out").click()
    expect(page).to_have_title("Login | Water Quality Control")
