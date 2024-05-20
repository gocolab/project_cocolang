from itertools import zip_longest
import re
from app.database.connection import Database
from app.models.common_codes import CommonCode
collection_common_codes = Database(CommonCode)

async def unique_comodules(conformed:bool=True):

    # Initialize sets for tracking uniqueness
    unique_frameworks = []
    unique_languages = []
    unique_database = []

    conditions = {'code_category':'comodules', 'conformed':conformed}
    
    commoncode_list = await collection_common_codes.getsbyconditions(conditions)

    for item in commoncode_list:
        # framework_name 분리 및 추가
        if item.code_classification == 'Frameworks':
            unique_frameworks.append(item.name)
        
        # language_name 분리 및 추가
        if item.code_classification == 'Languages':
            unique_languages.append(item.name)
        
        # database_name 분리 및 추가
        if item.code_classification == 'Databases':
            unique_database.append(item.name)
    # Use itertools.zip_longest to combine lists with padding of None automatically
    combinations = [
        {'language': lang if lang is not None else '', 
        'framework': fw if fw is not None else '', 
        'database': db if db is not None else ''}  
        for lang, fw, db in zip_longest(set(unique_languages), set(unique_frameworks), set(unique_database))
    ]
    return combinations

async def remove_and_concat(input_str, file_type):
    # '_'를 기준으로 문자열을 분리합니다.
    split_by_underscore = input_str.split('_')

    # 결과를 저장할 리스트를 초기화합니다.
    first_elements = []

    for part in split_by_underscore:
        # 첫 번째 요소에서 괄호와 괄호 안의 내용을 제거합니다.
        part_no_parentheses = re.sub(r"\s*\([^)]*\)", '', part)
        # 그런 다음 '\r\n' 또는 '\n'으로 문자열을 분리합니다.
        split_by_newline = re.split(r'\r\n|\n', part_no_parentheses)        
        
        # 첫 번째 요소가 null이 아니고, trim()을 적용했을 때 빈 문자열이 아닌 경우에만 결과 리스트에 추가합니다.
        if split_by_newline[0] and split_by_newline[0].strip() != '':
            first_elements.append(re.sub(r'\s+', '', split_by_newline[0]))

    # 결과 리스트의 각 요소를 '_'로 결합하여 최종 문자열을 생성합니다.
    join_result = 'dockers_' + '_'.join(first_elements)
    # 현재 시간을 "YYYYMMDD_HHMMSS" 포맷으로 변환
    file_suffix = datetime.now().strftime("%Y%m%d")
    # zip_file_name = f"{comodule_str}_{file_suffix}"
    file_name = f"{join_result}_{file_suffix}.{file_type}"
    return file_name

async def format_comodule_details(comodule):
    """
    Formats the details of a comodule object into a string.

    Parameters:
    - comodule: An object with the following attributes:
        - language_name(language_version)
        - framework_name(framework_version)
        - database_name(database_version)

    Returns:
    - A string that contains the formatted details.
    """
    # 각 컴포넌트의 이름과 버전을 조합합니다. 버전 정보가 없는 경우 이름만 사용합니다.
    language_details = f"{comodule.language_name}"
    framework_details = f"{comodule.framework_name}"
    database_details = f"{comodule.database_name}"
    # 모든 컴포넌트의 상세 정보를 하나의 문자열로 결합합니다.
    return f"{language_details}_{framework_details}_{database_details}"

import re
from datetime import datetime
async def create_filename(comodule, file_type:str = 'zip'):
    comodule_str_withoutversion = await format_comodule_details(comodule)
    
    # 정규표현식을 사용하여 괄호와 괄호 안의 내용을 삭제합니다.
    zip_file_name = await remove_and_concat(comodule_str_withoutversion, file_type)
    return zip_file_name

if __name__ == "__main__":
    # 예시 사용:

    # 주어진 문자열 예제
    input_str = "java(17)\npython(3.11)_jupyter lab\nspringboots(3.1.1)\nfastapi(0.110)\ngradle for java_mysql(8)\nmongodb(7)"
    # 결과 출력
    print(remove_and_concat(input_str))

