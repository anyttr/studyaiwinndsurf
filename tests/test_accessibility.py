import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAccessibility:
    @pytest.fixture
    def setup_accessibility(self, driver):
        # Navigate to accessibility settings
        driver.get('/settings/accessibility')
        return driver

    def test_font_size_changes(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find font size selector
        font_size_select = driver.find_element(By.ID, 'font-size-select')
        
        # Test each font size option
        sizes = ['small', 'medium', 'large', 'x-large']
        for size in sizes:
            # Select font size
            font_size_select.click()
            driver.find_element(By.XPATH, f"//li[text()='{size}']").click()
            
            # Get computed font size of a test element
            test_element = driver.find_element(By.TAG_NAME, 'body')
            computed_style = driver.execute_script(
                'return window.getComputedStyle(arguments[0]).fontSize',
                test_element
            )
            
            # Verify font size changed
            expected_sizes = {
                'small': '14px',
                'medium': '16px',
                'large': '18px',
                'x-large': '20px'
            }
            assert computed_style == expected_sizes[size]

    def test_high_contrast_mode(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find contrast toggle
        contrast_select = driver.find_element(By.ID, 'contrast-select')
        
        # Enable high contrast
        contrast_select.click()
        driver.find_element(By.XPATH, "//li[text()='High Contrast']").click()
        
        # Verify body has high-contrast class
        body = driver.find_element(By.TAG_NAME, 'body')
        assert 'high-contrast' in body.get_attribute('class')
        
        # Verify contrast colors
        background_color = driver.execute_script(
            'return window.getComputedStyle(arguments[0]).backgroundColor',
            body
        )
        assert background_color == 'rgb(0, 0, 0)'

    def test_reduced_motion(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find reduced motion toggle
        motion_toggle = driver.find_element(By.ID, 'reduced-motion-toggle')
        
        # Enable reduced motion
        motion_toggle.click()
        
        # Verify CSS variable is set
        root = driver.find_element(By.TAG_NAME, 'html')
        transition_duration = driver.execute_script(
            'return window.getComputedStyle(arguments[0]).getPropertyValue("--transition-duration")',
            root
        )
        assert transition_duration == '0s'

    def test_dyslexic_font(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find dyslexic font toggle
        font_toggle = driver.find_element(By.ID, 'dyslexic-font-toggle')
        
        # Enable dyslexic font
        font_toggle.click()
        
        # Verify font family changed
        body = driver.find_element(By.TAG_NAME, 'body')
        font_family = driver.execute_script(
            'return window.getComputedStyle(arguments[0]).fontFamily',
            body
        )
        assert 'OpenDyslexic' in font_family

    def test_line_spacing(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find line spacing selector
        spacing_select = driver.find_element(By.ID, 'line-spacing-select')
        
        # Test each spacing option
        spacings = ['tight', 'normal', 'loose', 'very-loose']
        expected_values = {
            'tight': '1.4',
            'normal': '1.6',
            'loose': '1.8',
            'very-loose': '2'
        }
        
        for spacing in spacings:
            # Select spacing
            spacing_select.click()
            driver.find_element(By.XPATH, f"//li[text()='{spacing}']").click()
            
            # Verify line height changed
            body = driver.find_element(By.TAG_NAME, 'body')
            line_height = driver.execute_script(
                'return window.getComputedStyle(arguments[0]).lineHeight',
                body
            )
            assert line_height == expected_values[spacing]

    def test_language_switch(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find language selector
        language_select = driver.find_element(By.ID, 'language-select')
        
        # Test each language
        languages = ['en', 'ro']
        for lang in languages:
            # Select language
            language_select.click()
            driver.find_element(By.XPATH, f"//li[@data-value='{lang}']").click()
            
            # Wait for translation to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//html[@lang='{lang}']"))
            )
            
            # Verify html lang attribute
            html = driver.find_element(By.TAG_NAME, 'html')
            assert html.get_attribute('lang') == lang

    def test_keyboard_navigation(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find all focusable elements
        focusable = driver.find_elements(
            By.CSS_SELECTOR,
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        
        # Verify tab index order
        for i, element in enumerate(focusable):
            # Send TAB key
            if i > 0:
                focusable[i-1].send_keys('\ue004')  # TAB key
            
            # Wait for element to receive focus
            WebDriverWait(driver, 10).until(
                EC.element_to_be_selected(element)
            )
            
            # Verify element has focus
            assert driver.switch_to.active_element == element

    def test_screen_reader_support(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find elements that should have ARIA labels
        elements = driver.find_elements(By.CSS_SELECTOR, '[aria-label]')
        
        # Verify all elements have appropriate ARIA labels
        for element in elements:
            assert element.get_attribute('aria-label') is not None
            assert len(element.get_attribute('aria-label')) > 0

    def test_focus_indicators(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find all interactive elements
        interactive = driver.find_elements(
            By.CSS_SELECTOR,
            'button, [href], input, select, textarea'
        )
        
        for element in interactive:
            # Focus the element
            driver.execute_script('arguments[0].focus()', element)
            
            # Get outline style
            outline = driver.execute_script(
                'return window.getComputedStyle(arguments[0]).outline',
                element
            )
            
            # Verify focus indicator is visible
            assert '3px solid' in outline
            assert '#4A90E2' in outline or 'rgb(74, 144, 226)' in outline

    def test_skip_link(self, setup_accessibility):
        driver = setup_accessibility
        
        # Find skip link
        skip_link = driver.find_element(By.CLASS_NAME, 'skip-link')
        
        # Verify initial state
        assert skip_link.value_of_css_property('position') == 'absolute'
        assert skip_link.value_of_css_property('top') == '-40px'
        
        # Focus skip link
        skip_link.send_keys('')  # Focus the element
        
        # Verify skip link is visible
        assert skip_link.value_of_css_property('top') == '0px'
