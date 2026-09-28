from test_data import *
from policy import POLICY


def _is_allowed(key, role):
    """Return True if `role` is allowed to read the value of `key`.

    - role=None  -> no access control (giữ tương thích với API chức năng gốc).
    - key không nằm trong POLICY -> coi như không nhạy cảm => cho phép.
    - Ngược lại, role phải nằm trong danh sách cho phép của key đó.
    """
    if role is None:
        return True
    if key not in POLICY:
        return True
    return role in POLICY[key]


def json_search(key, input_object, role=None):
    ret_val = []
    if isinstance(input_object, dict):  # Iterate dictionary
        for k, v in input_object.items():  # searching key in the dict
            if k == key and _is_allowed(key, role):
                ret_val.append({k: v})
            if isinstance(v, dict):  # the value is another dict so repeat
                ret_val.extend(json_search(key, v, role))
            elif isinstance(v, list):  # it's a list
                for item in v:
                    if not isinstance(item, (str, int)):  # if dict or list repeat
                        ret_val.extend(json_search(key, item, role))
    else:  # Iterate a list because some APIs return JSON object in a list
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(json_search(key, val, role))
    return ret_val


if __name__ == "__main__":
    print(json_search("issueSummary", data))
