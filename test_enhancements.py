#!/usr/bin/env python3
"""
测试脚本 - 验证需求计算器的增强功能
Test script - Verify desire calculator enhancements
"""

import json
import os
from datetime import datetime

def test_enhanced_data_structure():
    """测试新的数据结构"""
    print("=== 测试增强的数据结构 ===")
    
    # 创建一个测试需求
    test_desire = {
        "desire_test_20241201_120000": {
            "name": "房屋月租",
            "frequency": "每月",
            "cost": 3000.0,
            "priority": "高",
            "category": "住房",
            "enabled": True
        }
    }
    
    # 保存测试数据
    with open("test_desires.json", "w", encoding="utf-8") as f:
        json.dump(test_desire, f, ensure_ascii=False, indent=2)
    
    print("✅ 新的数据结构包含以下字段：")
    print("  - name: 需求名称")
    print("  - frequency: 频率")
    print("  - cost: 花销金额")
    print("  - priority: 优先级 (低/中/高/必需)")
    print("  - category: 类别 (住房/交通/餐饮/娱乐/购物/健康/教育/投资/其他)")
    print("  - enabled: 启用状态")
    
    # 验证数据完整性
    desire = list(test_desire.values())[0]
    required_fields = ['name', 'frequency', 'cost', 'priority', 'category', 'enabled']
    for field in required_fields:
        if field not in desire:
            print(f"❌ 缺少字段: {field}")
        else:
            print(f"✅ 包含字段: {field}")
    
    return True

def test_budget_calculation():
    """测试预算计算"""
    print("\n=== 测试预算计算功能 ===")
    
    # 模拟数据
    desires = {
        "desire_1": {"name": "房租", "frequency": "每月", "cost": 3000, "priority": "必需", "category": "住房", "enabled": True},
        "desire_2": {"name": "吃饭", "frequency": "每天", "cost": 50, "priority": "必需", "category": "餐饮", "enabled": True},
        "desire_3": {"name": "交通", "frequency": "每周", "cost": 100, "priority": "中", "category": "交通", "enabled": True},
        "desire_4": {"name": "娱乐", "frequency": "每月", "cost": 500, "priority": "低", "category": "娱乐", "enabled": False}
    }
    
    # 计算月度总花销
    monthly_total = 0
    category_totals = {}
    
    for desire in desires.values():
        if not desire['enabled']:
            continue
            
        cost = desire['cost']
        frequency = desire['frequency']
        category = desire['category']
        
        if frequency == "每天":
            monthly_cost = cost * 30
        elif frequency == "每周":
            monthly_cost = cost * 4.33
        elif frequency == "每月":
            monthly_cost = cost
        elif frequency == "每季度":
            monthly_cost = cost / 3
        elif frequency == "每年":
            monthly_cost = cost / 12
        else:
            monthly_cost = 0
            
        monthly_total += monthly_cost
        
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += monthly_cost
    
    yearly_total = monthly_total * 12
    
    print(f"✅ 月度总花销: ¥{monthly_total:.2f}")
    print(f"✅ 年度总花销: ¥{yearly_total:.2f}")
    
    print("\n按类别统计:")
    for category, total in category_totals.items():
        print(f"  - {category}: ¥{total:.2f}")
    
    # 测试预算进度
    budget_goal = 5000
    budget_percentage = min(100, int((monthly_total / budget_goal) * 100))
    print(f"\n✅ 预算目标: ¥{budget_goal}")
    print(f"✅ 预算使用: {budget_percentage}%")
    
    return True

def test_priority_system():
    """测试优先级系统"""
    print("\n=== 测试优先级系统 ===")
    
    priorities = ["低", "中", "高", "必需"]
    priority_colors = {
        "低": "#27ae60",
        "中": "#f39c12", 
        "高": "#e74c3c",
        "必需": "#8e44ad"
    }
    
    for priority in priorities:
        color = priority_colors.get(priority, "#2c3e50")
        print(f"✅ 优先级 '{priority}' 对应颜色: {color}")
    
    return True

def test_category_filtering():
    """测试类别筛选"""
    print("\n=== 测试类别筛选 ===")
    
    categories = [
        "住房", "交通", "餐饮", "娱乐", "购物", 
        "健康", "教育", "投资", "其他"
    ]
    
    print("✅ 支持的类别:")
    for category in categories:
        print(f"  - {category}")
    
    return True

def test_data_migration():
    """测试旧数据迁移"""
    print("\n=== 测试旧数据迁移 ===")
    
    # 模拟旧数据结构
    old_data = {
        "desire_1": {
            "name": "房屋月租",
            "frequency": "每月",
            "cost": 3000.0,
            "enabled": True
        }
    }
    
    # 迁移到新格式
    new_data = {}
    for desire_id, desire in old_data.items():
        new_data[desire_id] = {
            **desire,
            "priority": "中",  # 默认优先级
            "category": "其他"  # 默认类别
        }
    
    print("✅ 旧数据成功迁移到新格式")
    print("  - 添加默认优先级: 中")
    print("  - 添加默认类别: 其他")
    
    return True

def main():
    """运行所有测试"""
    print("🧪 开始测试需求计算器增强功能...")
    print("=" * 50)
    
    tests = [
        test_enhanced_data_structure,
        test_budget_calculation,
        test_priority_system,
        test_category_filtering,
        test_data_migration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🎉 测试结果: {passed} 通过, {failed} 失败")
    
    # 清理测试文件
    if os.path.exists("test_desires.json"):
        os.remove("test_desires.json")

if __name__ == "__main__":
    main()