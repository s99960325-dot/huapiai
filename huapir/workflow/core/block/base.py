from typing import Any, Callable, Dict, Optional

from huapir.ioc.container import DependencyContainer
from huapir.workflow.core.block.input_output import Input, Output


class Block:
    """block 的基类"""

    # block 的 id
    id: str
    # block 的名称
    name: str
    # block 的输入
    inputs: dict[str, Input] = {}
    # block 的输出
    outputs: dict[str, Output] = {}
    
    container: DependencyContainer

    def __init__(
        self,
        name: Optional[str] = None,
        inputs: Optional[dict[str, Input]] = None,
        outputs: Optional[dict[str, Output]] = None,
    ):
        self.id = getattr(self.__class__, "id", "anonymous_" + self.__class__.__name__)
        if name is not None:
            self.name = name
        if inputs is not None:
            self.inputs = inputs
        if outputs is not None:
            self.outputs = outputs

    def execute(self, **kwargs) -> dict[str, Any]:
        # Placeholder for block logic
        return {output: f"Processed {kwargs}" for output in self.outputs}


class ConditionBlock(Block):
    """条件判断块"""

    name: str = "condition"
    outputs: dict[str, Output] = {
        "condition_result": Output("condition_result", "条件结果", bool, "条件结果")
    }

    def __init__(
        self,
        condition_func: Callable[[dict[str, Any]], bool],
        inputs: dict[str, "Input"],
    ):
        super().__init__()
        self.inputs = inputs
        self.condition_func = condition_func

    def execute(self, **kwargs) -> dict[str, Any]:
        result = self.condition_func(kwargs)
        return {"condition_result": result}


class LoopBlock(Block):
    """循环控制块"""

    name: str = "loop"
    outputs: dict[str, Output] = {
        "should_continue": Output("should_continue", "是否继续", bool, "是否继续"),
        "iteration": Output("iteration", "当前迭代数据", dict, "当前迭代数据"),
    }

    def __init__(
        self,
        condition_func: Callable[[dict[str, Any]], bool],
        inputs: dict[str, "Input"],
        iteration_var: str = "index",
    ):
        super().__init__()
        self.inputs = inputs
        self.condition_func = condition_func
        self.iteration_var = iteration_var
        self.iteration_count = 0

    def execute(self, **kwargs) -> dict[str, Any]:
        should_continue = self.condition_func(kwargs)
        self.iteration_count += 1
        return {
            "should_continue": should_continue,
            "iteration": {self.iteration_var: self.iteration_count, **kwargs},
        }


class LoopEndBlock(Block):
    """循环结束块，收集循环结果"""

    name: str = "loop_end"
    outputs: dict[str, Output] = {
        "loop_results": Output("loop_results", "收集的循环结果", list, "收集的循环结果")
    }

    def __init__(self, inputs: dict[str, "Input"]):
        super().__init__()
        self.inputs = inputs
        self.results: list[dict[str, Any]] = []

    def execute(self, **kwargs) -> dict[str, Any]:
        self.results.append(kwargs)
        return {"loop_results": self.results}
