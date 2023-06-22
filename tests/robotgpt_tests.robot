*** Settings ***
Library    robotgpt.keywords.RobotGPTKeywords

*** Test Cases ***
Test Generator
    [Documentation]    A simple test to verify the createAndTestTransform keyword
    ${result} =    Create And Test Transform    sample_text.lores    expected_output.html
    Should Not Be Empty    ${result}


