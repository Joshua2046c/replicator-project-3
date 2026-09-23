# M6加粗螺杆及配套螺纹 — Build69

## 交付
STEP：manufacturing/cat-bowl/releases/export-0a27f04ada330aa49159d611b0afa05c/model.step
SHA256：9de38c2295b7a84f240d103e1814961f4cd560cd60ebfb4bb24367eb26a42772
同目录receipt.json绑定Build69与当前需求、brief；预览已刷新。独立检查：No P0 or P1 findings。

## 修改
螺杆从名义M5改为M6×1，头下12 mm，其中前端2 mm为5 mm平定位头；后部10 mm包含库生成的外螺旋牙形，非小径光杆。底座内螺纹同步为M6×1补偿牙形，切削大径6.45 mm。PETG0.45 mm直径补偿为默认试配值。内外螺纹采用相同轴向12 mm原始螺旋、同右旋方向与相同参考原点X=-24.8，外螺纹仅裁掉定位端及原始牙形越界。
底座曲面外延孔口调用M6打印螺纹kit，boss=none被拒绝后free实现；library IsoThread作为内螺纹负型，不加外凸块或螺母。

## 验证
- Build69四有效单实体、6对零件无体积穿插、0未确定项。
- 初次构建lock_screw/mast的检查超出短时预算；后续cad.inspect精确检查成功，0体积穿插、端面接触距离0。不将初次未确定结果当作通过。
- 螺杆/底座最小间隙0.1124 mm；底座/柱0.3 mm；碗/斜台0接触。
- Git源记录逐字段断言：mast和bowl完整对象记录、源码不变；全部对象装配位置不变；旋钮外形构造代码段逐字相同。
- 五个凹点仍直径5.8、深1.2、间距10，局部Z10/20/30/40/50；端点高度约123.8–163.8 mm，40 mm行程。当前定位头端面和直径保持原配合，不改柱。
- 本次核对静态第三档；未另做动态螺旋旋入或每档重新布尔检查。最高最低位置的原有证据仅覆盖未变的柱碗外形，不冒充新螺纹的全行程测试。

## 视觉证据
外螺纹与旋钮独立等轴视：.work/cache/cad-workbench/designs/cat-bowl/observations/51c09bc58a5e5aa06391193cc4a81d0c37a05017a6bc051d82c45b3d41d35a98/look-b850703c5048cb73c57d79c6/workbench_iso.png
局部装配：.work/cache/cad-workbench/designs/cat-bowl/observations/51c09bc58a5e5aa06391193cc4a81d0c37a05017a6bc051d82c45b3d41d35a98/look-ad128183af883c9347b43e2b/workbench_front.png
移除底座看定位端接触：.work/cache/cad-workbench/designs/cat-bowl/observations/51c09bc58a5e5aa06391193cc4a81d0c37a05017a6bc051d82c45b3d41d35a98/look-3e610d45df2ffc80528843e6/workbench_front.png
底座孔口轴向放大：.work/cache/cad-workbench/designs/cat-bowl/observations/51c09bc58a5e5aa06391193cc4a81d0c37a05017a6bc051d82c45b3d41d35a98/look-2bbe7e5cd240c0b07b7a0ed8/workbench_left.png

## 边界
几何检查不等同真实打印旋合、预紧强度或磨损认证；需先试印并校准补偿。保留食品接触、最高档1 kg静载、稳定性及耐久未测试的限制。本次无采购、切片或打印。
