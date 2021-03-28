import random
import re


class RandGen:
    '处理骰子'

    msg_out = ""

    def rand_gen(self, max_num, amount=1, punish=0, award=0, cmd=""):
        '根据骰子生成结果'
        result = 0
        while amount != 0:
            if punish:
                i = 0
                result_temp = 0
                msg = "惩罚骰" + cmd + "："
                max_num_count = max_num
                while max_num_count > 10:
                    max_num_count /= 10
                    i = i * 10 + 9
                result_temp = random.randint(0, i+1)
                max_high = random.randint(0, max_num_count-1)
                msg += str(result_temp + max_high * (i+1))
                punish_count = punish
                while punish_count > 0:
                    high_dig = random.randint(0, max_num_count-1)
                    msg += "，" + str(result_temp + high_dig * (i+1))
                    max_high = max(max_high, high_dig)
                    punish_count -= 1
                result_temp = result_temp + max_high * (i+1)
                result += result_temp
                msg += " (" + str(result_temp) + ")\n"
                self.msg_out += msg
            elif award:
                i = 0
                result_temp = 0
                msg = "奖励骰" + cmd + "："
                max_num_count = max_num
                while max_num_count > 10:
                    max_num_count /= 10
                    i = i * 10 + 9
                result_temp = random.randint(0, i+1)
                min_high = random.randint(0, max_num_count-1)
                msg += str(result_temp + min_high * (i+1))
                award_count = award
                while award_count > 0:
                    high_dig = random.randint(0, max_num_count-1)
                    msg += "，" + str(result_temp + high_dig * (i+1))
                    min_high = min(min_high, high_dig)
                    award_count -= 1
                result_temp = result_temp + min_high * (i+1)
                result += result_temp
                msg += " (" + str(result_temp) + ")\n"
                self.msg_out += msg
            else:
                result += random.randint(1, max_num)
            amount -= 1
        return result

    def string_process(self, cmd):
        "处理骰子字符串"
        if cmd.find("+") == -1:
            result = self.cmd_process(cmd)
            self.msg_out = '结果：' + cmd + " = " + \
                str(result) + "\n" + self.msg_out
            return
        else:
            cmds = cmd.split("+")
            result = 0
            for single_cmd in cmds:
                result += self.cmd_process(single_cmd)
            self.msg_out = '结果：' + cmd + " = " + \
                str(result) + "\n" + self.msg_out
            return

    def cmd_process(self, cmd):
        "处理单个骰子指令"
        if cmd.find("d") == -1:
            return int(cmd)
        else:
            dice_cmd = re.match(
                '^(?P<amount>\d+)d(?P<max_num>\d+)(?:\((?P<punish>\d+)\))?(?:\[(?P<award>\d+)\])?$', cmd).groupdict()
            amount = int(dice_cmd['amount'])
            max_num = int(dice_cmd['max_num'])
            punish = award = 0
            if dice_cmd['punish']:
                punish = int(dice_cmd['punish'])
            elif dice_cmd['award']:
                award = int(dice_cmd['award'])
            return self.rand_gen(max_num, amount, punish, award, cmd)

    def check_process(self, cmd):
        "处理检定指令"
        check_cmd = re.match(
            '^(?P<status>\d+)(?:\((?P<punish>\d+)\))?(?:\[(?P<award>\d+)\])?(?: (?P<name>.*))?$', cmd).groupdict()
        status = int(check_cmd['status'])
        name = ""
        punish = award = 0
        if check_cmd['name']:
            name = check_cmd['name']
        if check_cmd['punish']:
            punish = int(check_cmd['punish'])
        elif check_cmd['award']:
            award = int(check_cmd['award'])
        if status <= 0 or status > 100:
            self.msg_out = "错误！允许的数值范围为1-100。"
            return
        result = self.rand_gen(100, 1, punish, award, "1d100")
        if result <= 5:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(大成功)\n" + self.msg_out
        elif result <= status/5:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(极难成功)\n" + self.msg_out
        elif result <= status/2:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(困难成功)\n" + self.msg_out
        elif result <= status:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(成功)\n" + self.msg_out
        elif result > 95:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(大失败)\n" + self.msg_out
        else:
            self.msg_out = name + "检定：" + \
                str(result) + "/" + str(status) + "(失败)\n" + self.msg_out
