const handleObjectClassified = (obj, color) => {
  const el = document.createElement('div');
  el.classList.add('mbs-object');
  el.style.borderColor = color;
  el.style.left = `${obj.centerPoint.posX - 25}px`;
  el.style.top = `${obj.centerPoint.posY - 25}px`;
  el.textContent = obj.classTag;

  document.body.appendChild(el);
};

export default handleObjectClassified;
