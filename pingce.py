from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import FixKRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import AccEvaluator
from opencompass.datasets import CEvalDataset
import json
import os

# 定义 ICE 模板
ice_template = {
    "type": "PromptTemplate",
    "template": {
        "begin": "</E>",
        "round": [
            {
                "role": "HUMAN",
                "prompt": "问题：{{question}}\n答案："
            },
            {
                "role": "BOT",
                "prompt": "{answer}"
            }
        ]
    },
    "ice_token": "</E>"
}

# 设置检索器和推理器
retriever_config = {
    "type": "FixKRetriever",
    "fix_id_list": [0, 1, 2, 3, 4]
}

inferencer_config = {
    "type": "GenInferencer",
    "weights_path": "/root/xiehouyu1/merged"  # 替换为你训练好的模型的路径
}

# 定义评估器
evaluator_config = {
    "type": "AccEvaluator"
}

# 定义数据集配置
dataset_config = {
    "type": CEvalDataset,
    "path": "/root/xiehouyu1/xiehouyu_xtuner.jsonl",  # 替换为你的数据集路径
    "name": "xiehouyu_xtuner",
    "reader_cfg": {
        "input_columns": ["question", "answer"],
        "output_column": "answer"
    },
    "infer_cfg": {
        "ice_template": ice_template,
        "retriever": retriever_config,
        "inferencer": inferencer_config
    },
    "eval_cfg": evaluator_config
}

# 运行评估
dataset = CEvalDataset(dataset_config)
predictions = dataset.run_inference()
evaluation_results = dataset.evaluate(predictions)

# 输出评估结果到文件
output_file = "/root/xiehouyu1/out.json"

# 检查并创建输出文件的目录
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 将评估结果保存到文件中
with open(output_file, "w") as f:
    json.dump(evaluation_results, f)

print("Evaluation results saved to", output_file)
