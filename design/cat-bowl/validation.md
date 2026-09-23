# 五档浅凹点与六瓣手拧头 — Build67

## 交付
STEP：manufacturing/cat-bowl/releases/export-8ccd5813a845a86f513a70043abeb548/model.step
SHA256：0ab6fb7ce47bc8201befb4d0f6cf2fe916cac44fbc32040050f884f69dc7850a
导出记录同目录receipt.json；预览由STEP刷新。独立检查返回No P0 or P1 findings。前一轮需求更新后的旧记录绑定失败已由本次新构建与新要求的handoff取代。

## 尺寸与几何检查
- 5个浅凹点：局部Z10/20/30/40/50、直径5.8、深1.2 mm；入口0.35倒角。默认10 mm间距。
- 由低至高1–5档：柱底Z4/14/24/34/44，匹配局部凹点Z50/40/30/20/10。逐项断言柱底+凹点=螺丝固定轴高54 mm，通过。碗口最高点约123.7873/133.7873/143.7873/153.7873/163.7873 mm。最高插入22 mm，完整行程40 mm。
- Build63最低：4有效实体，6对无体积干涉；螺杆/柱为0距离接触；碗口Z123.7873085，底座/碗最小间隙1.3356 mm、旋钮/碗10.8167 mm。
- Build65最高：4有效实体，无体积干涉、螺杆/柱0距离接触；碗口Z163.7873085。
- Build67中间交付位置：4有效实体，6对无体积干涉；螺杆/柱及碗/承托台距离0。base/mast间隙0.3 mm；螺杆/底座0.235 mm是小径简化表示的间隙，不是真实牙面配合证明。第二、第四档为等距同形凹点中心的解析核对，未单独构建整机布尔检查。
- 六瓣旋钮最大外径28、厚8、侧棱R0.8、端面倒角0.4。头下X=-24.8、端面X=-12.8；名义M5x0.8×12。
- 与本次前Git提交逐项比较：base和bowl整个对象记录（含形状哈希、放置）、各自Python源代码完全一致。碗和底座未修改。顶部斜台、方榫尺寸原样保留。

## 视觉证据
五点正视：.work/cache/cad-workbench/designs/cat-bowl/observations/adc252275b6e6787ae697743da79408964ea606df0c431c4873ccfe76352c3c1/look-3962ef99dbaa65e7e924ee00/workbench_left.png
名义锁紧接触与旋钮：.work/cache/cad-workbench/designs/cat-bowl/observations/6bf11c97d6803159c2fd281f2bfa38d46e9e3a2a8c58e09bf599b753cbf20b4e/look-adb35b3bfeef9fd4cddf21f6/workbench_iso.png
整体侧面：.work/cache/cad-workbench/designs/cat-bowl/observations/6bf11c97d6803159c2fd281f2bfa38d46e9e3a2a8c58e09bf599b753cbf20b4e/look-2298edc760364d613fe6e40d/workbench_front.png

## 限制与失败处理
旋钮首版圆边fillet0.8失败，mast已提交59；仅修复旋钮端面为0.4倒角，成功提交。未重复此前耗尽的完整螺纹旋合方法。
外螺杆采用库定义的ISO小径简化表示，仅末端保留5 mm名义平端包络。没有完整外螺纹螺旋牙形；实物必须另有M5x0.8外螺纹，不能照着细光杆直接打印来锁紧。本STEP为位置/外观配合样机，不是完整螺纹加工文件。底座真实补偿内螺纹未改。名义装配不再悬空，但真实螺纹配合、锁紧力、凹点磨损、稳定性、食品接触仍需实测。
