import csv
import json
import config  # 导入配置文件


def parse_factor_name(full_name):
    """
    解析因子名称，提取基础名称和长度值（如果存在）
    返回: (base_name, length_value) 或 (full_name, None)
    """
    if '@' in full_name:
        base_name, length_str = full_name.split('@', 1)
        try:
            return base_name, int(length_str)
        except ValueError:
            print(f"警告: 因子 '{full_name}' 的长度值 '{length_str}' 不是有效整数")
            return full_name, None
    return full_name, None


def get_factor_category(base_name):
    """确定因子所属的类别"""
    for category, factors in config.factor_categories.items():
        if base_name in factors:
            return category
    return None


def build_factor_params(base_name, length_value, category):
    """
    根据因子类别构建参数字典
    返回: 包含必要参数的字典
    """
    params = {"factor_name": base_name}
    default = config.default_data

    if category == "no_length":
        # 不需要额外参数
        pass

    elif category == "length_atr":
        if length_value is None:
            length_value = default.get("length", 20)  # 默认长度
            print(f"提示: 为因子 '{base_name}' 使用默认长度 {length_value}")
        params.update({
            "length": length_value,
            "atr_length": default["atr_length"]
        })

    elif category == "length_thr":
        if length_value is None:
            length_value = default.get("length", 20)
            print(f"提示: 为因子 '{base_name}' 使用默认长度 {length_value}")
        params.update({
            "length": length_value,
            "thr": default["thr"]
        })

    elif category == "length_n_std":
        if length_value is None:
            length_value = default.get("length", 20)
            print(f"提示: 为因子 '{base_name}' 使用默认长度 {length_value}")
        params.update({
            "length": length_value,
            "n_std": default["n_std"]
        })

    elif category == "short_long":
        params.update({
            "short": default["short"],
            "long": default["long"]
        })

    elif category == "short_long_atr":
        params.update({
            "short": default["short"],
            "long": default["long"],
            "atr_length": default["atr_length"]
        })

    elif category == "short_long_vol":
        params.update({
            "short": default["short"],
            "long": default["long"],
            "vol_length": default["vol_length"]
        })

    elif category == "fast_slow_signal":
        params.update({
            "fast": default["fast"],
            "slow": default["slow"],
            "signal": default["signal"]
        })

    return params


def convert_csv_to_json(csv_file_path, json_file_path):
    """从CSV读取因子并生成JSON配置"""
    result = {}

    try:
        with open('../factor_name.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                if not row:
                    continue

                full_name = row[0].strip()
                if not full_name:
                    continue

                # 解析因子名称
                base_name, length_value = parse_factor_name(full_name)

                # 确定因子类别
                category = get_factor_category(base_name)
                print(category)

                if category:
                    # 特殊因子：使用类别配置
                    params = build_factor_params(base_name, length_value, category)
                    result[full_name] = params
                else:
                    # 普通因子：仅包含基础名称和长度
                    if length_value is not None:
                        result[full_name] = {
                            "factor_name": base_name,
                            "length": length_value
                        }
                    else:
                        print(f"警告: 跳过未分类且无长度的因子 '{full_name}'")

        # 写入JSON文件
        with open('./factor_name.json', 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)

        print(f"成功处理 {len(result)} 个因子，输出到 {json_file_path}")

    except FileNotFoundError:
        print(f"错误: 文件 {csv_file_path} 不存在")
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


# 使用示例
if __name__ == "__main__":
    input_csv = "factor_name.csv"  # 输入CSV文件名
    output_json = "factor_name.json"  # 输出JSON文件名

    convert_csv_to_json(input_csv, output_json)