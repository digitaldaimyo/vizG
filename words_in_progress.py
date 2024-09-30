from abc import ABC
from typing import Optional, Union, List

from address import Address
from address import *
from address import A, F, G, H, I, J, K, L, M, P, S, T, X, Y, Z
from numeric import Numeric
from macroVariable import MacroVariable
from decimal import Decimal 
from modals import ModalGroup
from word import Word
from rule import Rule
from rules import (
    BlockRule,
    NumericRule,
    NumericRangeRule,
    ExcludeModalGroup,
    ExcludeAddress,
    RequireAddress,
    RequireOneOfAddresses,
    RequireAllAddresses,
    DuplicateAddress,
    NumericLeadingZeroRule,
    NumericPrecisionRule,
    RequireExactlyOneOfAddresses,
)

class AddressWord(Word):
    def __init__(self, address: Address, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[Decimal, int, float]] = None, max_value: Optional[Union[Decimal, int, float]] = None, precision: Optional[int] = None, rules: Optional[List[Rule]] = None):
        
        leading_zero = False
        if precision is None or precision == 0:
            precision = 0
            leading_zero = True
                
        numeric = value
        if isinstance(value, Decimal):
            numeric = Numeric(value, precision, leading_zero)
            
        rules = rules if rules is not None else []
        rules.append(DuplicateAddress(address))
        rules.append(NumericPrecisionRule(precision)) 
        if min_value is not None and max_value is not None:
            rules.append(NumericRangeRule(min_value, max_value))
            
        super().__init__(address, numeric, rules=rules)
        
    def validate(self, block=None):
        for rule in self.rules:
            if isinstance(rule, NumericRule):
                rule.validate(self.numeric)
            if block is not None and isinstance(rule, BlockRule):
                rule.validate(block)

class AxisWord(AddressWord):
    def __init__(self, address, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(address, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class XWord(AxisWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(X, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class YWord(AxisWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(Y, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class ZWord(AxisWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(Z, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class AWord(AxisWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(A, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
                
class FWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(F, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
        
class GWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(G, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
        
class HWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(H, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class LWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(L, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
        
class PWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(P, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
        
class SWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(S, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)
        
class TWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], min_value: Optional[Union[int, float, Decimal]] =None, max_value: Optional[Union[int, float, Decimal]] =None, precision: Optional[int] =None, rules: Optional[List[Rule]]=None):
        super().__init__(T, value, min_value=min_value, max_value=max_value, precision=precision, rules=rules)

class MotionWord(GWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], rules: Optional[List[Rule]]=None):
        rules = rules if rules is not None else []
        rules.append(ExcludeModalGroup(ModalGroup.MOTION))
        super().__init__(value, min_value=value, max_value=value, precision=0, rules=rules)

class G00(MotionWord):
    def __init__(self):
        rules = [RequireOneOfAddresses([X, Y, Z, A])]
        super().__init__(0, rules=rules)

class G01(MotionWord):
    def __init__(self):
        axis_require_rule = RequireOneOfAddresses([X, Y, Z, A])
        require_f_rule = RequireAddress(F)
        rules = [axis_require_rule, require_f_rule]
        super().__init__(1, rules=rules)

class G02(MotionWord):
    def __init__(self):
        require_f_rule = RequireAddress(F)
        axis_require_rule = RequireOneOfAddresses([X, Y, Z, I, J, K])
        rules = [require_f_rule, axis_require_rule]
        super().__init__(2, rules=rules)

class G03(MotionWord):
    def __init__(self):
        require_f_rule = RequireAddress(F)
        axis_require_rule = RequireOneOfAddresses([X, Y, Z, I, J, K])
        rules = [require_f_rule, axis_require_rule]
        super().__init__(3, rules=rules)

class G04(GWord):
    def __init__(self):
        rules = [RequireAddress(P)]
        super().__init__(4, precision=0, rules=rules)
        
class G43(GWord):
    def __init__(self):
        rules = [RequireAddress(H)]
        super().__init__(43, precision=0, rules=rules)
                
class MWord(AddressWord):
    def __init__(self, value: Union[Decimal, MacroVariable, Numeric], rules: Optional[List[Rule]] =None):
        rules = rules if rules is not None else []
        rules.append(ExcludeAddress(M))
        super().__init__(M, value, min_value=value, max_value=value, precision=0, rules=rules)

class M00(MWord):
    def __init__(self):
        super().__init__(0)

class M01(MWord):
    def __init__(self):
        super().__init__(1)

class M02(MWord):
    def __init__(self):
        super().__init__(2)
        
class M03(MWord):
    def __init__(self):
        rules = [RequireAddress(S)]
        super().__init__(3, rules=rules)
        
class M04(MWord):
    def __init__(self):
        rules = [RequireAddress(S)]
        super().__init__(4, rules=rules)
        
class M05(MWord):
    def __init__(self):
        super().__init__(5)
        
class M06(MWord):
    def __init__(self):
        rules = [RequireAddress(T)]
        super().__init__(6, rules=rules)
        
class M99(MWord):
    def __init__(self):
        super().__init__(99)

class ParameterRuleSet:
    def __init__(self, parameter_rules=None, default_rules=None):
        self.parameter_rules = parameter_rules or {}
        self.default_rules = default_rules or []

    def get_rules_for_param(self, param_value):
        return self.parameter_rules.get(param_value, self.default_rules)

class CompoundWord(Word, ABC):
    def __init__(self, address: Address, value: Union[Decimal, MacroVariable, Numeric], compound_address: Address, parameter_rules=None, numeric_rules=None, default_rules=None):
        super().__init__(address, value)
        self.compound_address = compound_address
        self.numeric_rules = numeric_rules or []
        parameter_rules = parameter_rules or []
        self.parameter_rule_set = ParameterRuleSet(parameter_rules, default_rules)
        self.rules.append(RequireAddress(compound_address))

    def get_parameter(self, block):
        word = next((word for word in block if word.address == self.compound_address), None)
        if word:
            return word
        else:
            raise ValueError(f"No {self.compound_address.letter()} address found in the block")

    def apply_numeric_rules(self, param_word):
        for rule in self.numeric_rules:
            rule.validate(param_word)

    def apply_block_rules(self, block):
        for rule in self.rules:
            if isinstance(rule, BlockRule):
                rule.validate(block)

    def validate(self, block):
        super().validate()
        param_word = self.get_parameter(block)
        self.apply_numeric_rules(param_word.numeric)
        self.apply_block_rules(block)
        param_value = int(param_word.numeric.value)
        rules_to_apply = self.parameter_rule_set.get_rules_for_param(param_value)
        for rule in rules_to_apply:
            rule.validate(block)

class G65(CompoundWord):
    def __init__(self):
        numeric_value = Numeric(65, precision=0, leading_zero=False)
        parameter_rules = {
            9810: [
                RequireOneOfAddresses([X, Y, Z]),
                RequireAddress(F),
            ],
            9811: [RequireOneOfAddresses([X, Y, Z])],
            9812: [RequireExactlyOneOfAddresses([X, Y])],
            9814: [RequireAddress(D)],
        }
        numeric_rules = [NumericRangeRule(0, 99999)]
        default_rules = []
        super().__init__(G, numeric_value, P, parameter_rules, numeric_rules, default_rules)

class G154(CompoundWord):
    def __init__(self):
        numeric_value = Numeric(154, precision=0, leading_zero=False)
        parameter_rules = {}
        numeric_rules = [NumericRangeRule(1, 99)]
        default_rules = []
        super().__init__(G, numeric_value, P, parameter_rules, numeric_rules, default_rules)

class M98(CompoundWord):
    def __init__(self, subprogram_o_number, repeat_count=None):
        numeric_value = Numeric(98, precision=0)
        default_rules = [
            PWord(subprogram_o_number, min_value=1, max_value=9999)
        ]
        if repeat_count is not None:
            default_rules.append(LWord(repeat_count, min_value=1, max_value=9999))
        numeric_rules = [NumericRangeRule(1, 99999)]
        super().__init__(M, numeric_value, P, parameter_rules={}, numeric_rules=numeric_rules, default_rules=default_rules)