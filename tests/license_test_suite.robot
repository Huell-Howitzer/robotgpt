*** Settings ***
Library           OperatingSystem
Resource          global_variables.robot


*** Test Cases ***
Check License File Exists
    [Documentation]    Verify that the LICENSE file exists
    File Should Exist     LICENSE

Check License File Has Content
    [Documentation]    Verify that the LICENSE file is not empty
    ${file_content}=      Get File     LICENSE
    Should Not Be Empty   ${file_content}

Passing Test
    [Documentation]    This test case does nothing but passes
    No Operation
