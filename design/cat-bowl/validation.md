# 加深碗体 — Build58

## 交付
STEP：manufacturing/cat-bowl/releases/export-9a0b8e5faad5c3739b4f91cfe2e6168f/model.step
SHA256：4529da750c17ed34800499cde7cd3c8f564129312f457ef5416e4e63a95e2e4e
预览已更新。本次只修改碗的外深18→32 mm和根部圆角2→12 mm。32/R12为图片比例参考后的默认值，不是照片精确测量。

## 检查
- Git保存的Build56与当前源记录逐字段比较：base、mast、lock_screw对象（含形状哈希）完全不变；所有对象装配变换不变；全部参数只有bowl_depth与bowl_inner_fillet变化。
- Workbench历史比较接口返回缺失构建manifest，未将其当作通过；上述源记录及导出记录哈希比较为替代证据。
- 四个有效实体，六对零件无体积穿插；bowl/mast距离0，承托面接触；底部配合参数未变。
- 碗口140 mm、倾角10度、底厚6.5 mm；名义中央内深由11.5 mm增到25.5 mm。R12使侧壁根部较圆润。
- 当前碗口最高点143.7873085 mm；按同一40 mm升降行程推算端点123.7873–163.7873 mm。用户已明确选择保留加深碗和其余零件，总高要求更新为约123.8–163.8 mm；此项冲突已解决，螺丝未装配仍不代表整机验收通过。

## 视觉证据
碗侧视：.work/cache/cad-workbench/designs/cat-bowl/observations/786e91e5c6ba4140064646aeb68c05809efbc97408e5342658fb7dcfde782933/look-de3ed1280c73bc92a31e84ef/workbench_front.png
碗等轴视：.work/cache/cad-workbench/designs/cat-bowl/observations/786e91e5c6ba4140064646aeb68c05809efbc97408e5342658fb7dcfde782933/look-de3ed1280c73bc92a31e84ef/workbench_iso.png

## 独立审查及遗留限制
Build58审查仍指出P0：背面螺丝悬空，距离底座12.0021 mm，height_lock未装配。此为既有状态，本次遵照其余不动未修改螺丝或立柱。
证据：.work/cache/cad-workbench/designs/cat-bowl/observations/786e91e5c6ba4140064646aeb68c05809efbc97408e5342658fb7dcfde782933/look-8f03c01451f49988237f1510/workbench_front.png
食品接触、实物锁紧、载荷、稳定性及打印配合均未测试。未切片、未打印。

## 用户确认后的记录刷新限制
用户已确认总高更新为约123.8–163.8 mm。几何仍为同一Build58，现有STEP与预览就是已确认的加深几何。更新需求与brief后，两次handoff导出（auto及force）均返回review_target_changed，仍引用旧review-58-15889ada-b5c1-4e39-9b93-8105dadc2d36；停止重复。当前导出记录绑定的是更新总高前的文档，尚未完成新需求的检查绑定，不得宣称整个项目已通过。原STEP未丢失、未改动。
