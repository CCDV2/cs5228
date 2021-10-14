import dataset
import model_zoo
import metric_zoo
from torch.utils.data import DataLoader
import pandas as pd


def main(cfg):
    dataset_name = cfg['dataset']
    train_dataset = getattr(dataset, dataset_name)(
        **cfg[dataset_name], is_train=True)
    test_dataset = getattr(dataset, dataset_name)(
        **cfg[dataset_name], is_train=False)
    train_dataloader = DataLoader(
        train_dataset, shuffle=True, **cfg.get('dataloader', {}))
    test_dataloader = DataLoader(
        test_dataset, shuffle=False, **cfg.get('dataloader', {}))

    model_name = cfg['model']
    model = getattr(model_zoo, model_name)(
        **cfg[model_name])  # type: model_zoo.BaseModel
    pred, gt = model.predict(train_dataloader, test_dataloader)

    metric_name = cfg['metric']
    metric = getattr(metric_zoo, metric_name)
    score = metric(pred, gt, **cfg[metric_name])
    print(f'{metric_name}: {score}')

    dump_path = cfg.get('dump_path', '')
    if dump_path:
        df = pd.DataFrame({'Predicted': pred})
        df.to_csv(dump_path, index_label='Id')
