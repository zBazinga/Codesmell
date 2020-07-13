import os
import sys
import torch
from config import Config
import torch.nn.functional as F


def train(train_iter, test_iter, model, args, config):
    if torch.cuda.is_available():  # 判断是否有GPU，如果有把模型放在GPU上训练，速度质的飞跃
        model.cuda()

    config = Config()

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # 梯度下降优化器，采用Adam
    steps = 0
    best_acc = 0
    best_recall = 0
    best_precision = 0
    best_f1 = 0
    last_step = 0
    model.train()
    for epoch in range(1, args.epoch + 1):
        print("第", epoch, "轮开始")
        for batch in train_iter:
            feature, feature2, feature3, feature4, feature5, feature6, feature7, target = batch.content_method, batch.context_method, batch.access_method, batch.content_class_contain, batch.context_class_contain, batch.content_class_target, batch.context_class_target, batch.tag
            # print("feature-size:", feature.size())
            if torch.cuda.is_available():  # 如果有GPU将特征更新放在GPU上
                feature, target = feature.cuda(), target.cuda()
            optimizer.zero_grad()  # 将梯度初始化为0，每个batch都是独立训练地，因为每训练一个batch都需要将梯度归零
            logits = model(feature, feature2, feature3, feature4, feature5, feature6, feature7)
            # print(logits.shape)
            loss = F.cross_entropy(logits, target)  # 计算损失函数 采用交叉熵损失函数
            loss.backward()  # 反向传播
            optimizer.step()  # 放在loss.backward()后进行参数的更新
            steps += 1
            if steps % config.steps_show == 0:  # 每训练多少步计算一次准确率，我这边是1，可以自己修改
                # print(torch.max(logits, 1)[1].view(target.size()).data)
                # print(target.data)
                precison, recall, f1 = result(torch.max(logits, 1)[1].view(target.size()).data, target.data)
                corrects = (torch.max(logits, 1)[1].view(
                    target.size()).data == target.data).sum()  # logits是[128,10],torch.max(logits, 1)也就是选出第一维中概率最大的值，输出为[128,1],torch.max(logits, 1)[1]相当于把每一个样本的预测输出取出来，然后通过view(target.size())平铺成和target一样的size (128,),然后把与target中相同的求和，统计预测正确的数量
                train_acc = 100.0 * corrects / batch.batch_size  # 计算每个mini batch中的准确率
                print('steps:{} - loss: {:.6f}  acc:{:.4f} precision:{:.4f} recall:{:.4f} f1:{:.4f}'.format(
                    steps,
                    loss.item(),
                    train_acc,
                    precison,
                    recall,
                    f1))

            if steps % config.steps_eval == 0:  # 每训练100步进行一次验证
                dev_acc,  avg_loss, avg_f1, avg_precision, avg_recall = eval(test_iter, model)
                if avg_f1 > best_f1:
                    best_f1 = avg_f1
                    best_precision = avg_precision
                    best_recall = avg_recall
                    last_step = steps
                    print('Saving best model, f1: {:.4f}  recall: {:.4f} precision: {:.4f}\n'.format(best_f1,best_recall,best_precision))
                    save(model, config.save_dir, steps)
                # else:
                #     if steps - last_step >= config.early_stopping:
                #         print('\n提前停止于 {} steps, f1: {:.4f}%'.format(last_step, best_f1))
                #         raise KeyboardInterrupt
                # if dev_acc > best_acc:
                #     best_acc = dev_acc
                #     last_step = steps
                #     print('Saving best model, acc: {:.4f}%\n'.format(best_acc))
                #     save(model, config.save_dir, steps)
                # else:
                #     if steps - last_step >= config.early_stopping:
                #         print('\n提前停止于 {} steps, acc: {:.4f}%'.format(last_step, best_acc))
                #         raise KeyboardInterrupt


def eval(test_iter, model):
    model.eval()
    corrects = 0
    avg_loss = 0
    precision = 0
    recall = 0
    f1 = 0
    for batch in test_iter:
        feature, feature2, feature3, feature4, feature5, feature6, feature7, target = batch.content_method, batch.context_method, batch.access_method, batch.content_class_contain, batch.context_class_contain, batch.content_class_target, batch.context_class_target, batch.tag
        if torch.cuda.is_available():
            feature, target = feature.cuda(), target.cuda()
        logits = model(feature, feature2, feature3, feature4, feature5, feature6, feature7)
        #print(logits)
        loss = F.cross_entropy(logits, target)
        avg_loss += loss.item()
        corrects += (torch.max(logits, 1)
                     [1].view(target.size()).data == target.data).sum()
        precison2, recall2, f12 = result(torch.max(logits, 1)[1].view(target.size()).data, target.data)
        precision += precison2
        recall += recall2
        f1 += f12
    size = len(test_iter.dataset)
    size2 = len(test_iter)
    avg_precision = precision/size2
    avg_recall = recall/size2
    avg_f1 = f1/size2
    avg_loss /= size
    accuracy = 100.0 * corrects / size
    print('\nEvaluation - loss: {:.6f}  acc: {:.4f}%({}/{} precision:{:.4f} recall:{:.4f} f1:{:.4f}) \n'.format(avg_loss,
                                                                                                             accuracy,
                                                                                                             corrects,
                                                                                                             size,
                                                                                                             avg_precision,
                                                                                                             avg_recall,
                                                                                                             avg_f1))
    return accuracy, avg_loss, avg_f1, avg_precision, avg_recall

    # 定义模型保存函数


def save(model, save_dir, steps):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_path = 'bestmodel_steps{}.pt'.format(steps)
    save_bestmodel_path = os.path.join(save_dir, save_path)
    torch.save(model.state_dict(), save_bestmodel_path)


def result(pred, tag):
    TN = 0
    TP = 0
    FN = 0
    FP = 0
    for i in range(tag.shape[0]):
        if pred[i] == 0 and tag[i] == 0:
            TN += 1
        if pred[i] == 1 and tag[i] == 0:
            FN += 1
        if pred[i] == 0 and tag[i] == 1:
            FP += 1
        if pred[i] == 1 and tag[i] == 1:
            TP += 1
    if TP + FP != 0:
        precision = TP / (TP + FP)
    else:
        precision = 0
    if TP + FN != 0:
        recall = TP / (TP + FN)
    else:
        recall = 0
    if precision + recall != 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0
    return precision, recall, f1
